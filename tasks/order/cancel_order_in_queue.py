# -*- coding: utf-8 -*-]

import datetime

from tasks.celery_app import app
from tasks.base_task import SqlAlchemyTask

from tasks.models.inventory import InventoryModel
from models.order import OrderModel
from constants import QUEUE_ORDER
from exception.celery_exception import CeleryException

@app.task(base=SqlAlchemyTask, bind=True, queue=QUEUE_ORDER, ignore_result=True)
def cancel_order_before_user_confirm(self, order_id):
    session = self.session
    order = get_order(session, order_id)
    if order.status != 0 or order.status != 100:
        return

    stay_days = get_stay_days(order.checkin_date, order.checkout_date)
    year_months = [(day.year, day.month) for day in stay_days]
    year_months = {}.fromkeys(year_months).keys()

    inventories = InventoryModel.get_by_merchant_hotel_roomtype_dates(
        session, order.merchant_id,
        order.hotel_id, order.room_type_id, year_months)

    for day in stay_days:
        inventory = get_inventory_by_date(inventories, day.year, day.month)
        inventory.add_val_by_day(day.day, 1, order.room_num)

    order.status = 500
    session.commit()

@app.task(base=SqlAlchemyTask, bind=True, queue=QUEUE_ORDER)
def cancel_order_by_user(self, order_id):
    session = self.session
    order = get_order(session, order_id)
    if order.status not in  [0, 100]:
        print order.todict()
        raise CeleryException(100, 'illegal status')

    stay_days = get_stay_days(order.checkin_date, order.checkout_date)
    year_months = [(day.year, day.month) for day in stay_days]
    year_months = {}.fromkeys(year_months).keys()

    inventories = InventoryModel.get_by_merchant_hotel_roomtype_dates(
        session, order.merchant_id,
        order.hotel_id, order.room_type_id, year_months)

    for day in stay_days:
        inventory = get_inventory_by_date(inventories, day.year, day.month)
        inventory.add_val_by_day(day.day, 1, order.room_num)

    order.status = 400
    session.commit()

    return order

def get_stay_days(checkin_date, checkout_date):
    aday = datetime.timedelta(days=1)
    days = []
    while checkin_date < checkout_date:
        days.append(checkin_date)
        checkin_date= checkin_date + aday

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

def get_order(session, order_id):
    return OrderModel.get_by_id(session, order_id)

