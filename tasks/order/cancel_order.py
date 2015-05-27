# -*- coding: utf-8 -*-]

import time
import datetime
import requests

from tasks.celery_app import app
from tasks.base_task import SqlAlchemyTask, OrderTask
from tasks.order import cancel_order_in_queue as Cancel
from tasks.stock import PushInventoryTask

from models.order import OrderModel
from models.order_history import OrderHistoryModel
from exception.celery_exception import CeleryException
from config import API


@app.task(base=OrderTask, bind=True)
def cancel_order_by_server(self, order_id):
    session = self.session
    order = OrderModel.get_by_id(session, order_id)

    pre_status = order.status

    if order.status == 0 or order.status == 100:
        _order = cancel_before_user_confirm(session, order.id)
    elif order.status == 200:
        raise CeleryException(1000, 'illegal status')
    elif order.status == 300:
        _order = cancel_after_user_confirm(session, order.id)
    elif order.status in [400, 500, 600]:
        return order
    else:
        raise CeleryException(1000, 'illegal status')


    if _order.status != pre_status:
        OrderHistoryModel.set_order_status_by_server(session, _order, pre_status, _order.status)
    return _order

@app.task(base=OrderTask, bind=True)
def cancel_order_by_user(self, user, order_id, reason):
    session = self.session
    order = OrderModel.get_by_id(session, order_id)

    pre_status = order.status

    if order.merchant_id != user.merchant_id:
        raise CeleryException(100, 'merchant invalid')
    if order.status not in [0, 100]:
        raise CeleryException(1000, 'illegal status')

    if not callback_order_server(order_id):
        raise CeleryException(1000, 'callback order server error')


    task = Cancel.cancel_order_by_user.delay(order_id, reason)
    result = task.get()
    
    if task.status == 'SUCCESS':
        if result.status != pre_status:
            OrderHistoryModel.set_order_status_by_user(session, user, result, pre_status, result.status)
        PushInventoryTask().push_inventory.delay(order.roomtype_id)
        return result
    else:
        if isinstance(result, Exception):
            raise result

def callback_order_server(order_id):
    url = API['ORDER'] + '/order/ebooking/update'
    params = {'orderId': order_id, 'msgType': 0, 'success': False,
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

def cancel_before_user_confirm(session, order_id):
    task = Cancel.cancel_order_before_user_confirm.delay(order_id)
    result = task.get()
    
    if task.status == 'SUCCESS':
        return result
    else:
        if isinstance(result, Exception):
            raise result

def cancel_after_user_confirm(session, order_id):
    task = Cancel.cancel_order_after_user_confirm.delay(order_id)
    result = task.get()
    if task.status == 'SUCCESS':
        return result
    else:
        if isinstance(result, Exception):
            raise result


