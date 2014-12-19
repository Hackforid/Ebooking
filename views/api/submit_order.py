# -*- coding: utf-8 -*-

from tornado.escape import json_encode, json_decode, url_escape
from tornado import gen

from tools.auth import auth_login
from views.base import BtwBaseHandler
from tasks.order.submit_order import deal_order

from exception.json_exception import JsonException

class SubmitOrderAPIHandler(BtwBaseHandler):

    @gen.coroutine
    @auth_login(json=True)
    def post(self):
        deal_order.delay(self.request.body)

        self.finish_json()

