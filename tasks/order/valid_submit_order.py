# -*- coding: utf-8 -*-


import datetime

from tasks.celery_app import app

from models.cooperate_roomtype import CooperateRoomTypeModel
from models.inventory import InventoryModel
from models.rate_plan import RatePlanModel
from models.order import OrderModel
from tasks.base_task import SqlAlchemyTask
from tasks.order.submit_order import start_order

from entity.order import SubmitOrder


def get_stay_days(start_date, end_date):
    date_format = "%Y-%m-%d"
    start_time = datetime.datetime.strptime(start_date, date_format)
    end_time = datetime.datetime.strptime(end_date, date_format)

    if start_time >= end_time:
        return start_time, start_time

    aday = datetime.timedelta(days=1)
    days = []
    while start_time < end_time:
        days.append(start_time)
        start_time = start_time + aday

    return days


def valid_arguments(order):
    pass

def combin_year_month(year, month):
    return int("{}{:0>2d}".format(year, month))

def valid_inventory(session, order):
    print '# valid inventory for order ', order.id
    stay_days = get_stay_days(order.checkin_date, order.checkout_date)
    year_months = [(day.year, day.month) for day in stay_days]
    year_months = {}.fromkeys(year_months).keys()

    inventories = InventoryModel.get_by_merchant_hotel_roomtype_dates(
        session, order.merchant_id,
        order.hotel_id, order.room_type_id, year_months)
    
    if not inventories:
        print "no inventory"
        return False

    for inventory in inventories:
        print inventory.todict()


    for day in stay_days:
        inventory = None
        month = combin_year_month(day.year, day.month)
        print '...finding', month

        for _inventory in inventories:
            if _inventory.month == month:
                inventory = _inventory
                break
        else:
            print 'day', day, 'not found'
            return False

        if inventory.get_day(day.day, 0) < order.room_quantity:
            print 'day', day, ' is not enough (inventory = '+inventory.get_day(day.day, 0) + ')'
            return False
    else:
        print 'found'
        return True


def create_order(session, submit_order):
    order = OrderModel.get_by_main_order_id(session, submit_order.id)
    if order:
        # callback 订单已存在
        print 'order exist'
        #return False
        return order

    order = OrderModel.new_order(session, submit_order)
    if order:
        return order
    else:
        # callback 创建失败
        pass


def get_rateplan(session, order):
    rate_plan = RatePlanModel.get_by_id(session, order.rate_plan_id)
    if not rate_plan:
        # callback no rateplan
        pass
    return rate_plan



@app.task(base=SqlAlchemyTask, bind=True, ignore_result=True)
def deal_order(self, order):
    print '==' * 20
    print order
    session = self.session
    submit_order = SubmitOrder(order)
    print submit_order

    if not valid_arguments(submit_order):
        pass

    rate_plan = get_rateplan(session, submit_order)
    if not rate_plan:
        print 'no rate plan'
        return

    submit_order.merchant_id = rate_plan.merchant_id
    order = create_order(session, submit_order)
    if not order:
        print 'create order fail'
        return

    if not valid_inventory(session, submit_order):
        # callback inventory fail
        print 'more room please'
        order.status = 200
        session.commit()
        return


    # second valid in spec queue
    start_order.apply_async(args=[order.id])
