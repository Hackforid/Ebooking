# -*- coding: utf-8 -*-

from tasks.celery_app import app
from tasks.base_task import SqlAlchemyTask
from constants import QUEUE_ORDER

from models.order import OrderModel

@app.task(base=SqlAlchemyTask, bind=True)
def get_waiting_orders(self, merchant_id, start, limit):
    return OrderModel.get_waiting_orders(self.session, merchant_id, start, limit)


@app.task(base=SqlAlchemyTask, bind=True)
def get_today_book_orders(self, merchant_id, start, limit):
    orders = OrderModel.get_today_book_orders(self.session, merchant_id, start, limit)
    return orders

@app.task(base=SqlAlchemyTask, bind=True)
def get_today_checkin_orders(self, merchant_id, start, limit):
    orders = OrderModel.get_today_checkin_orders(self.session, merchant_id, start, limit)
    return orders
