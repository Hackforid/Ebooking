# -*- coding: utf-8 -*-

from tornado.escape import json_encode, json_decode, url_escape
from tornado import gen

from tools.auth import auth_login
from views.base import BtwBaseHandler
from tasks.order.submit_order import submit_order 
from tasks.order.cancel_order import cancel_order_by_server
from models.order import OrderModel
from models.merchant import MerchantModel

from exception.json_exception import JsonException
from exception.celery_exception import CeleryException

import tcelery
tcelery.setup_nonblocking_producer()

class SubmitOrderAPIHandler(BtwBaseHandler):
    '''
    this api is use for server to submit order
    '''

    @gen.coroutine
    def post(self):
        task = yield gen.Task(submit_order.apply_async,
                args=[self.request.body])

        if task.status == 'SUCCESS':
            order = task.result
            if order.status in [200, 400, 500]:
                raise JsonException(1, 'fail')
            else:
                merchant = MerchantModel.get_by_id(self.db, order.merchant_id)
                self.finish_json(result=dict(
                    order_id=order.id,
                    wait= 0 if order.confirm_type == OrderModel.CONFIRM_TYPE_AUTO or order.status == 300 else 1,
                    merchant=merchant.todict(),
                    ))
        else:
            if isinstance(task.result, CeleryException):
                raise JsonException(1, task.result.errmsg)
            else:
                raise JsonException(1, 'server error')


class CancelOrderAPIHander(BtwBaseHandler):

    @gen.coroutine
    def post(self, order_id):
        task = yield gen.Task(cancel_order_by_server.apply_async,
                args=[order_id])

        if task.status == 'SUCCESS':
            self.finish_json(result=dict(
                order_id=task.result.id,
                ))
        else:
            if isinstance(task.result, CeleryException):
                raise JsonException(1, task.result.errmsg)
            else:
                raise JsonException(1, 'server error')


