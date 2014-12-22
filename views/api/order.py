# -*- coding: utf-8 -*-

from tornado.escape import json_encode, json_decode, url_escape
from tornado import gen

from tools.auth import auth_login
from views.base import BtwBaseHandler
from exception.json_exception import JsonException

import tasks.models.order as Order

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

