# -*- coding: utf-8 -*-]

import datetime

from tasks.celery_app import app
from tasks.base_task import SqlAlchemyTask

from tasks.models.inventory import InventoryModel
from models.order import OrderModel


def cancel_before_user_confirm(session, order):
    pass

def cancel_after_user_confirm(session, order):
    pass


@app.task(base=SqlAlchemyTask, bind=True)
def cancel_order_by_server(self, order_id):
    session = self.session
    order = get_order(session, order_id)

    if order.status == 200:
        pass
    elif order.status == 0 or order.status == 100:
        cancel_before_user_confirm(session, order)
    elif order.status == 300:
        cancel_after_user_confirm(session, order)

@app.task(base=SqlAlchemyTask, bind=True)
def cancel_order_by_user(self, order_id):
    session = self.session
    order = get_order(session, order_id)

