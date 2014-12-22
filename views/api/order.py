# -*- coding: utf-8 -*-

from tornado.escape import json_encode, json_decode, url_escape
from tornado import gen

from tools.auth import auth_login
from views.base import BtwBaseHandler
from exception.json_exception import JsonException
from exception.celery_exception import CeleryException

from tasks.models import order as Order
from tasks.order import submit_order as SubmitOrder
from tasks.order import cancel_order as CancelOrder

class OrderWaitingAPIHandler(BtwBaseHandler):

    @gen.coroutine
    @auth_login(json=True)
    def get(self):
        merchant_id = self.current_user.merchant_id
        
        task = yield gen.Task(Order.get_waiting_orders.apply_async,
                args=[merchant_id])
        print task.result
        if task.status == 'SUCCESS':
            self.finish_json(result={
                'orders': [order.todict() for order in task.result] if task.result
                                            else [],
                })
        else:
            raise JsonException(errcode=1000, errmsg="wrong")


class OrderOperateAPIHandler(BtwBaseHandler):

    @gen.coroutine
    @auth_login(json=True)
    def post(self, order_id):
        merchant_id = self.current_user.merchant_id

        task = yield gen.Task(SubmitOrder.confirm_order_by_user.apply_async,
                args=[merchant_id, order_id])
        if task.status == 'SUCCESS':
            self.finish_json(result=dict(
                order=task.result.todict(),
                ))
        else:
            if isinstance(task.result, CeleryException):
                raise JsonException(1000, task.result.errmsg)
            else:
                raise JsonException(1000, 'network error')


    @gen.coroutine
    @auth_login(json=True)
    def delete(self, order_id):
        merchant_id = self.current_user.merchant_id

        task = yield gen.Task(CancelOrder.cancel_order_by_user.apply_async,
                args=[merchant_id, order_id])
        if task.status == 'SUCCESS':
            self.finish_json(result=dict(
                order=task.result.todict(),
                ))
        else:
            if isinstance(task.result, CeleryException):
                raise JsonException(1000, task.result.errmsg)
            else:
                raise JsonException(1000, 'network error')
