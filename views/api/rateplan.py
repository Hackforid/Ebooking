# -*- coding: utf-8 -*-

from tornado import gen
from tornado.httpclient import AsyncHTTPClient
from tornado.escape import json_encode, json_decode, url_escape

from tools.auth import auth_login
from tools.request_tools import get_and_valid_arguments
from views.base import BtwBaseHandler
from exception.json_exception import JsonException

import tasks.models.rate_plan as RatePlanModel


import tcelery
tcelery.setup_nonblocking_producer()

class RatePlanAPIHandler(BtwBaseHandler):

    @gen.coroutine
    @auth_login(json=True)
    def post(self, hotel_id, roomtype_id):
        args = self.get_json_arguments()
        name, meal_type, punish_type = get_and_valid_arguments(args, 'name', 'meal_type', 'punish_type')
        merchant_id = self.current_user.merchant_id

        rateplan, roomrate = (yield gen.Task(RatePlanModel.new_rate_plan.apply_async,
            args=[merchant_id, hotel_id, roomtype_id, name, meal_type, punish_type])).result

        if rateplan:
            self.finish_json(result=dict(
                rateplan=rateplan.todict(),
                roomrate=roomrate.todict(),
                ))
        else:
            raise JsonException(errcode="1001", errmsg="wrong")

    @gen.coroutine
    @auth_login(json=True)
    def get(self, hotel_id, roomtype_id):
        merchant_id = self.current_user.merchant_id

        rateplans, roomrates = (yield gen.Task(RatePlanModel.get_by_room.apply_async,
            args=[merchant_id, hotel_id, roomtype_id])).result or (None, None)

        if rateplans and roomrates:
            self.finish_json(result=dict(
                rateplans = [rateplan.todict() for rateplan in rateplans],
                roomrates = [roomrate.todict() for roomrate in roomrates],
                ))
        else:
            raise JsonException(errcode="1002", errmsg="not found")


