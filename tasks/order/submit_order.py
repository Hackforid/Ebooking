# -*- coding: utf-8 -*-]

import datetime

from tasks.celery_app import app
from tasks.base_task import SqlAlchemyTask

from tasks.models.inventory import InventoryModel
from models.order import OrderModel
from constants import QUEUE_ORDER

def get_stay_days(checkin_date, checkout_date):
    date_format = "%Y-%m-%d"
    start_time = datetime.datetime.strptime(start_date, date_format)
    end_time = datetime.datetime.strptime(end_date, date_format)

    if start_time >= end_date:
        return start_time, start_time

    aday = datetime.timedelta(days=1)
    days = []
    while start_time < end_date:
        days.append(start_time)
        start_time = start_time + aday

    return days

def valid_order(order):
    pass

def valid_inventory(order, stay_days):
    year_months = [(day.year, day.month) for day in stay_days]
    year_months = {}.fromkeys(year_months).keys()

    inventories = InventoryModel.get_by_merchant_id_and_hotel_id_and_days(order.merchant_id,
            order.hotel_id, year_months)
    if not inventories or len(inventories) != len(year_months):
        return False

    for day in stay_days:
        inventory = None
        str_month = "%d|%d" % (day.year, day.month)

        for _inventory in inventories:
            if _inventory.month == str_month:
                inventory = _inventory
                break
        else:
            return False

        if inventory.get_day(day.day, 0) < order.room_quantity:
            return False
    else:
        order.merchant_id=inventories[0].merchant_id
        return True


def create_order(order):
    order = OrderModel.get_by_main_order_id(order.id)
    if order:
        return

    order = OrderModel.new_order(order)
    if order:
        return order

def create_order_success(order):
    pass


def create_order_fail(order):
    pass

def get_order(session, order_id):
    return OrderModel.get_by_id(session, order_id)


@app.task(base=SqlAlchemyTask, bind=True, queue=QUEUE_ORDER, ignore_result=True)
def start_order(self, order_id):
    print 'hello world'

    session = self.session
    order = get_order(session, order_id)
    print isinstance(order.checkin_date, datetime.date)



    
    #stay_days = get_stay_days(order['checkInDate'], order['checkOutDate'])

    #if not valid_inventory(order, stay_days):
        #pass

    #create_order(order)



