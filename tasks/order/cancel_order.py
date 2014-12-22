# -*- coding: utf-8 -*-]

import datetime

from tasks.celery_app import app
from tasks.base_task import SqlAlchemyTask
from tasks.order import cancel_order_in_queue as Cancel

from models.order import OrderModel
from exception.celery_exception import CeleryException


def cancel_before_user_confirm(session, order):
    pass

def cancel_after_user_confirm(session, order):
    pass


@app.task(base=SqlAlchemyTask, bind=True)
def cancel_order_by_server(self, order_id):
    session = self.session
    order = OrderModel.get_by_id(session, order_id)

    if order.status == 200:
        pass
    elif order.status == 0 or order.status == 100:
        cancel_before_user_confirm(session, order)
    elif order.status == 300:
        cancel_after_user_confirm(session, order)

@app.task(base=SqlAlchemyTask, bind=True)
def cancel_order_by_user(self, merchant_id, order_id):
    session = self.session
    order = OrderModel.get_by_id(session, order_id)

    if order.merchant_id != merchant_id:
        raise CeleryException(100, 'merchant invalid')
    if order.status not in [0, 100]:
        raise CeleryException(1000, 'illegal status')

    task = Cancel.cancel_order_by_user.delay(order_id)
    result = task.get()
    
    if task.status == 'SUCCESS':
        return result
    else:
        if isinstance(result, Exception):
            raise result
