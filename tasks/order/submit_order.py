# -*- coding: utf-8 -*-


import time
import datetime
import requests

from tasks.celery_app import app

from models.cooperate_roomtype import CooperateRoomTypeModel
from models.inventory import InventoryModel
from models.rate_plan import RatePlanModel
from models.order_history import OrderHistoryModel
from models.order import OrderModel
from tasks.base_task import SqlAlchemyTask
from tasks.order.submit_order_in_queue import start_order
from tasks.stock import PushInventoryTask

from exception.celery_exception import CeleryException

from entity.order import SubmitOrder
from config import API

@app.task(base=SqlAlchemyTask, bind=True)
def confirm_order_by_user(self, user, order_id):
    session = self.session
    order = OrderModel.get_by_id(session, order_id)
    pre_status = order.status
    if order.merchant_id != user.merchant_id:
        raise CeleryException(100, 'merchant not valid')
    if order.status != 100:
        raise CeleryException(200, 'illegal status')

    if callback_order_server(order_id):
        order.confirm_by_user(session)
        if order.status != pre_status:
            OrderHistoryModel.set_order_status_by_user(session, user, order, pre_status, order.status)
        return order
    else:
        raise CeleryException(1000, 'callback order server fail')

def callback_order_server(order_id):
    url = API['ORDER'] + '/order/ebooking/update'
    params = {'orderId': order_id, 'msgType': 0, 'success': True,
            'trackId': generate_track_id(order_id)}
    r = requests.post(url, data=params)
    print r.text
    if r.status_code == 200:
        j = r.json()
        if j['errcode'] == 0:
            return True
    return False

def generate_track_id(order_id):
    return "{}|{}".format(order_id, time.time())


@app.task(base=SqlAlchemyTask, bind=True)
def submit_order(self, order_json):
    print order_json
    session = self.session
    try:
        submit_order = SubmitOrder(order_json)
    except ValueError as e:
        raise CeleryException(errcode=2000, errmsg=e.message)
    print submit_order

    if not valid_arguments(submit_order):
        raise CeleryException(200, 'invalid_arguments')

    rate_plan = get_rateplan(session, submit_order)
    if not rate_plan:
        raise CeleryException(300, 'no rate plan')

    submit_order.merchant_id = rate_plan.merchant_id
    order = create_order(session, submit_order)
    if not order:
        raise CeleryException(session, 'create order fail')

    if order.status != 0:
        return order

    if not valid_inventory(session, submit_order):
        print 'more room please'
        order.status = 200
        session.commit()

        OrderHistoryModel.set_order_status_by_server(session, order, 0, 200)
        return order


    # second valid in spec queue
    task = start_order.apply_async(args=[order.id])
    result = task.get()
    if task.status == 'SUCCESS':
        return result
    else:
        raise result


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
    return True

def combin_year_month(year, month):
    return int("{}{:0>2d}".format(year, month))

def valid_inventory(session, order):
    print '# valid inventory for order ', order.id
    stay_days = get_stay_days(order.checkin_date, order.checkout_date)
    year_months = [(day.year, day.month) for day in stay_days]
    year_months = {}.fromkeys(year_months).keys()

    inventories = InventoryModel.get_by_merchant_hotel_roomtype_dates(
        session, order.merchant_id,
        order.hotel_id, order.roomtype_id, year_months)
    
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

        if inventory.get_day(day.day, 1) < order.room_quantity\
                and inventory.get_day(day.day, 0) < order.room_quantity:
            print 'room not enough in {}'.format(day)
            return False
    else:
        print 'found'
        return True


def create_order(session, submit_order):
    order = OrderModel.get_by_main_order_id(session, submit_order.id)
    if order:
        # callback 订单已存在
        print 'order exist'
        return order

    order = OrderModel.new_order(session, submit_order)
    if order:
        return order
    else:
        # callback 创建失败
        pass


def get_rateplan(session, order):
    rate_plan = RatePlanModel.get_by_id(session, order.rateplan_id)
    if not rate_plan:
        # callback no rateplan
        pass
    return rate_plan
