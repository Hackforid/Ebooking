# -*- coding: utf-8 -*-


import datetime

from tasks.celery_app import app

from tasks.models.cooperate_roomtype import CooperateRoomTypeModel
from tasks.models.inventory import InventoryModel
from tasks.models.rate_plan import RatePlanModel
from tasks.models.order import OrderModel
from tasks.base_task import SqlAlchemyTask

from models.order import SubmitOrder 

def get_stay_days(start_date, end_date):
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


def valid_arguments(order):
    pass


def valid_inventory(order):
    stay_days = get_stay_days(order.checkin_date, order.checkout_date)
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
        return True


def create_order(submit_order):
    order = OrderModel.get_by_main_order_id(submit_order.id)
    if order:
        # callback 订单已存在
        print 'order exist'
        return False

    order = OrderModel.new_order(submit_order)
    if order:
        return order
    else:
        # callback 创建失败
        pass

def start_order(order):
    pass

def get_rateplan(order):
    rate_plan = RatePlanModel.get_by_id(order.rate_plan_id)
    if not rate_plan:
        #callback no rateplan
        pass
    return rate_plan

#@app.task(base=SqlAlchemyTask, bind=True, ignore_result=True)
@app.task()
def deal_order(order):
    print '=' * 20
    print order
    submit_order = SubmitOrder(order)

    if not valid_arguments(submit_order):
        pass

    rate_plan = get_rateplan(submit_order)
    if not rate_plan:
        print 'no rate plan'
        return

    submit_order.merchant_id = rate_plan.merchant_id
    if not create_order(submit_order):
        print 'create order fail'
        return

    return
    #if not valid_inventory(submit_order):
        ##callback inventory fail
        #print 'more room please'
        #return

    #start_order(submit_order)
