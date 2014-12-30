# -*- coding: utf-8 -*-]

import time
import datetime
import requests

from tasks.celery_app import app
from tasks.base_task import SqlAlchemyTask
from tasks.order import cancel_order_in_queue as Cancel

from models.order import OrderModel
from exception.celery_exception import CeleryException
from config import API


@app.task(base=SqlAlchemyTask, bind=True)
def cancel_order_by_server(self, order_id):
    session = self.session
    order = OrderModel.get_by_id(session, order_id)

    if order.status == 0 or order.status == 100:
        return cancel_before_user_confirm(session, order.id)
    elif order.status == 200:
        raise CeleryException(1000, 'illegal status')
    elif order.status == 300:
        return cancel_after_user_confirm(session, order.id)
    else:
        raise CeleryException(1000, 'illegal status')

@app.task(base=SqlAlchemyTask, bind=True)
def cancel_order_by_user(self, merchant_id, order_id, reason):
    session = self.session
    order = OrderModel.get_by_id(session, order_id)

    if order.merchant_id != merchant_id:
        raise CeleryException(100, 'merchant invalid')
    if order.status not in [0, 100]:
        raise CeleryException(1000, 'illegal status')

    if not callback_order_server(order_id):
        raise CeleryException(1000, 'callback order server error')


    task = Cancel.cancel_order_by_user.delay(order_id, reason)
    result = task.get()
    
    if task.status == 'SUCCESS':
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


