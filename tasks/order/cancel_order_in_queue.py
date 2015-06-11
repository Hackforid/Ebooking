# -*- coding: utf-8 -*-]

import datetime

from tasks.celery_app import app
from tasks.base_task import SqlAlchemyTask, OrderTask

from tasks.models.inventory import InventoryModel
from models.order import OrderModel
from constants import QUEUE_ORDER
from exception.celery_exception import CeleryException
from utils.stock_push.inventory import InventoryPusher


@app.task(base=OrderTask, bind=True, queue=QUEUE_ORDER)
def cancel_order_after_user_confirm(self, order_id):
    session = self.session
    order = get_order(session, order_id)
    if order.status != 300:
        raise CeleryException(100, 'illegal status')

    stay_days = get_stay_days(order.checkin_date, order.checkout_date)
    year_months = [(day.year, day.month) for day in stay_days]
    year_months = {}.fromkeys(year_months).keys()

    inventories = InventoryModel.get_by_merchant_hotel_roomtype_dates(
        session, order.merchant_id,
        order.hotel_id, order.roomtype_id, year_months)

    recovery_inventory(stay_days, inventories, order)

    order.status = 600
    r = InventoryPusher(session).push_by_roomtype_id(order.roomtype_id)
    if r:
        session.commit()
        return order
    else:
        raise Exception("push stock fail")


def recovery_inventory(stay_days, inventories, order):
    room_num_record = [record.split('|')
                       for record in order.room_num_record.split(',')]
    room_num_record = [(int(record[0]), int(record[1]))
                       for record in room_num_record]
    for i, day in enumerate(stay_days):
        inventory = get_inventory_by_date(inventories, day.year, day.month)
        num_auto, num_manual = room_num_record[i]
        if inventory:
            inventory.recovery_val_by_day(day.day, num_auto, num_manual)


@app.task(base=OrderTask, bind=True, queue=QUEUE_ORDER)
def cancel_order_before_user_confirm(self, order_id):
    session = self.session
    order = get_order(session, order_id)
    print order.status
    if order.status not in [0, 100]:
        raise CeleryException(100, 'illegal status')

    stay_days = get_stay_days(order.checkin_date, order.checkout_date)
    year_months = [(day.year, day.month) for day in stay_days]
    year_months = {}.fromkeys(year_months).keys()

    inventories = InventoryModel.get_by_merchant_hotel_roomtype_dates(
        session, order.merchant_id,
        order.hotel_id, order.roomtype_id, year_months)

    recovery_inventory(stay_days, inventories, order)

    order.status = 500
    r = InventoryPusher(session).push_by_roomtype_id(order.roomtype_id)
    if r:
        session.commit()
        return order
    else:
        raise CeleryException(1000, "push stock fail")


@app.task(base=OrderTask, bind=True, queue=QUEUE_ORDER)
def cancel_order_by_user(self, order_id, reason):
    session = self.session
    order = get_order(session, order_id)
    if order.status not in [0, 100]:
        raise CeleryException(100, 'illegal status')

    stay_days = get_stay_days(order.checkin_date, order.checkout_date)
    year_months = [(day.year, day.month) for day in stay_days]
    year_months = {}.fromkeys(year_months).keys()

    inventories = InventoryModel.get_by_merchant_hotel_roomtype_dates(
        session, order.merchant_id,
        order.hotel_id, order.roomtype_id, year_months)

    recovery_inventory(stay_days, inventories, order)

    order.status = 400
    order.extra = reason
    r = InventoryPusher(session).push_by_roomtype_id(order.roomtype_id)
    if r:
        session.commit()
        return order
    else:
        raise CeleryException(1000, "push stock fail")


def get_stay_days(checkin_date, checkout_date):
    aday = datetime.timedelta(days=1)
    days = []
    while checkin_date < checkout_date:
        days.append(checkin_date)
        checkin_date = checkin_date + aday

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
