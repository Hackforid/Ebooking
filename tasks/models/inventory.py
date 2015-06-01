# -*- coding: utf-8 -*-

import datetime

from tasks.celery_app import app
from tasks.base_task import SqlAlchemyTask
from tasks.stock import PushInventoryTask
from models.inventory import InventoryModel
from models.cooperate_roomtype import CooperateRoomTypeModel

from constants import QUEUE_ORDER
from utils.stock_push.inventory import InventoryPusher
from tools.log import Log


@app.task(base=SqlAlchemyTask, bind=True, queue=QUEUE_ORDER)
def modify_inventory(self, merchant_id, hotel_id, roomtype_id, price_type, change_num, start_date, end_date):
    session = self.session
    stay_days = get_stay_days(start_date, end_date)
    year_months = [(day.year, day.month) for day in stay_days]
    year_months = {}.fromkeys(year_months).keys()

    inventories = InventoryModel.get_by_merchant_hotel_roomtype_dates(
        session, merchant_id,
        hotel_id, roomtype_id, year_months)

    for day in stay_days:
        inventory = get_inventory_by_date(inventories, day.year, day.month)
        if not inventory:
            continue

        if change_num != 0:
            inventory.add_val_by_day(day.day, price_type, change_num)
        else:
            inventory.set_val_by_day(day.day, price_type, change_num)
    r = InventoryPusher(self.session).push_by_roomtype_id(roomtype_id)
    if r:
        session.commit()
        return inventories
    else:
        session.rollback()
        return None

def get_stay_days(start_date, end_date):
    aday = datetime.timedelta(days=1)
    days = []
    while start_date <= end_date:
        days.append(start_date)
        start_date = start_date + aday

    return days

def combin_year_month(year, month):
    return int("{}{:0>2d}".format(year, month))

def get_inventory_by_date(inventories, year, month):
    _month = combin_year_month(year, month)
    for inventory in inventories:
        if inventory.month == _month:
            return inventory
    else:
        return


@app.task(base=SqlAlchemyTask, bind=True)
def complete_in_four_months(self):
    roomtypes = CooperateRoomTypeModel.get_all(self.session)
    InventoryModel.insert_all_in_months(self.session, roomtypes, 13)

