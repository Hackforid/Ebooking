# -*- coding: utf-8 -*-

from tornado.escape import json_encode, json_decode, url_escape
from tornado import gen

from tools.auth import auth_login
from views.base import BtwBaseHandler
from tasks.order.submit_order import submit_order 
from tasks.order.cancel_order import cancel_order_by_server

from exception.json_exception import JsonException
from exception.celery_exception import CeleryException

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
            if order.status == 200:
                raise JsonException(1, 'fail')
            else:
                self.finish_json(result=dict(
                    order_id=task.result.id,
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
            order = task.result
            self.finish_json(result=dict(
                order_id=task.result.id,
                ))
        else:
            if isinstance(task.result, CeleryException):
                raise JsonException(1, task.result.errmsg)
            else:
                raise JsonException(1, 'server error')


