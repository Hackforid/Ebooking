# -*- coding: utf-8 -*-]

import datetime
import time

from tasks.celery_app import app
from tasks.base_task import OrderTask

from tasks.models.inventory import InventoryModel
from models.cooperate_roomtype import CooperateRoomTypeModel
from models.order import OrderModel
from models.order_history import OrderHistoryModel
from constants import QUEUE_ORDER
from tools.log import Log
from utils.stock_push.inventory import InventoryPusher
from exception.json_exception import JsonException

@app.task(base=OrderTask, bind=True, queue=QUEUE_ORDER)
def start_order(self, order_id):
    session = self.session
    order = get_order(session, order_id)
    if not order:
        Log.info("query order {} is None".format(order_id))
        return None
    if order.status != 0:
        return order

    # valid is roomtype online
    roomtype = CooperateRoomTypeModel.get_by_id(self.session, order.roomtype_id)
    if roomtype.is_online != 1:
        Log.info('roomtype is not online')
        order.status = 200
        order.exception_info = 'roomtype is not online'
        session.commit()
        OrderHistoryModel.set_order_status_by_server(session, order, 0, 200)
        return order

    order = modify_inventory(session, order)
    if order.status != 0:
        OrderHistoryModel.set_order_status_by_server(session, order, 0, order.status)

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

def valid_inventory(inventories, stay_days, room_quantity):
    if not inventories:
        Log.info('no inventory')
        return False

    for inventory in inventories:
        print inventory.todict()

    for day in stay_days:
        inventory = get_inventory_by_date(inventories, day.year, day.month)
        if not inventory:
            Log.info('day {}-{} inventory not found'.format(day.year, day.month))
            return False
        if inventory.get_day(day.day) < room_quantity:
            Log.info('room not enough')
            return False
    else:
        Log.info('found')
        return True

def modify_inventory(session, order):
    stay_days = get_stay_days(order.checkin_date, order.checkout_date)
    year_months = [(day.year, day.month) for day in stay_days]
    year_months = {}.fromkeys(year_months).keys()

    inventories = InventoryModel.get_by_merchant_hotel_roomtype_dates(
        session, order.merchant_id,
        order.hotel_id, order.roomtype_id, year_months)

    if not valid_inventory(inventories, stay_days, order.room_num):
        Log.info('valid inventory fail')
        order.exception_info = 'valid inventory fail'
        order.status = 200
        session.commit()
        return order

    room_num_record = []
    is_auto = True

    for day in stay_days:
        inventory = get_inventory_by_date(inventories, day.year, day.month)
        num_auto, num_manual = inventory.deduct_val_by_day(day.day, order.room_num)
        if num_manual > 0:
            is_auto = False
        room_num_record.append((num_auto, num_manual))

    if is_auto:
        order.status = 300
        order.confirm_type = OrderModel.CONFIRM_TYPE_AUTO
    else:
        order.status = 100
        order.confirm_type = OrderModel.CONFIRM_TYPE_MANUAL

    order.room_num_record = generate_room_num_record(room_num_record)

    r = InventoryPusher(session).push_by_roomtype_id(order.roomtype_id)
    if r:
        session.commit()
        return order
    else:
        session.rollback()
        raise Exception("push stock fail")

def generate_room_num_record(room_num_record):
    room_num_record_str = ','.join(['{}|{}'.format(*record) for record in room_num_record])
    print room_num_record_str
    return room_num_record_str

def get_order(session, order_id):
    return OrderModel.get_by_id(session, order_id)


