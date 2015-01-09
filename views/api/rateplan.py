# -*- coding: utf-8 -*-

from tornado import gen
from tornado.httpclient import AsyncHTTPClient
from tornado.escape import json_encode, json_decode, url_escape

from tools.auth import auth_login, auth_permission
from tools.request_tools import get_and_valid_arguments
from views.base import BtwBaseHandler
from exception.json_exception import JsonException
from exception.celery_exception import CeleryException

import tasks.models.rate_plan as RatePlanModel

from constants import PERMISSIONS 


class RatePlanAPIHandler(BtwBaseHandler):

    @gen.coroutine
    @auth_login(json=True)
    @auth_permission(PERMISSIONS.admin | PERMISSIONS.pricing, json=True)
    def post(self, hotel_id, roomtype_id):
        args = self.get_json_arguments()
        name, meal_num, punish_type = get_and_valid_arguments(
            args, 'name', 'meal_num', 'punish_type')
        merchant_id = self.current_user.merchant_id
        self.valid_new_rateplan_args(name, meal_num, punish_type)

        task = yield gen.Task(RatePlanModel.new_rate_plan.apply_async,
                           args=[merchant_id, hotel_id, roomtype_id, name, meal_num, punish_type])
        if task.status == 'SUCCESS':
            rateplan, roomrate = task.result
            self.finish_json(result=dict(
                rateplan=rateplan.todict(),
                roomrate=roomrate.todict(),
            ))
        else:
            if isinstance(task.result, CeleryException):
                raise JsonException(task.result.errcode, task.result.errmsg)
            else:
                raise JsonException(errcode="1000", errmsg="server error")

    @gen.coroutine
    @auth_login(json=True)
    @auth_permission(PERMISSIONS.admin | PERMISSIONS.pricing, json=True)
    def get(self, hotel_id, roomtype_id):
        merchant_id = self.current_user.merchant_id

        rateplans, roomrates = (
            yield gen.Task(RatePlanModel.get_by_room.apply_async,
                           args=[merchant_id, hotel_id, roomtype_id])).result or (None, None)

        if rateplans and roomrates:
            self.finish_json(result=dict(
                rateplans=[rateplan.todict() for rateplan in rateplans],
                roomrates=[roomrate.todict() for roomrate in roomrates],
            ))
        else:
            self.finish_json(result=dict(
                rateplans=[],
                roomrates=[],
            ))

    def valid_new_rateplan_args(self, name, meal_num, punish_type):
        if not isinstance(name, basestring):
            raise JsonException(errcode=2001, errmsg="wrong name")
        if len(name) > 20:
            raise JsonException(errcode=2002, errmsg="wrong name length")
        if punish_type not in [0, 1, 2, 3, 4]:
            raise JsonException(errcode=2003, errmsg="wrong punish_type")
        if meal_num not in [-1, 0, 1, 2, 100]:
            raise JsonException(errcode=2004, errmsg="wrong meal_num")


class RatePlanModifyAPIHandler(BtwBaseHandler):

    @gen.coroutine
    @auth_login(json=True)
    @auth_permission(PERMISSIONS.admin | PERMISSIONS.pricing, json=True)
    def put(self, hotel_id, roomtype_id, rateplan_id):
        args = self.get_json_arguments()
        name, meal_num, punish_type = get_and_valid_arguments(args,
                                                              'name', 'meal_num', 'punish_type')

        self.valid_arguments(name, meal_num, punish_type)

        task = yield gen.Task(RatePlanModel.modify_rateplan.apply_async,
                              args=[rateplan_id, name, meal_num, punish_type])
        result = task.result
        if isinstance(result, CeleryException):
            raise JsonException(errcode=result.errcode, errmsg=result.errmsg)
        else:
            self.finish_json(result=dict(
                rateplan=result[0].todict(),
                roomrate=result[1].todict(),
            ))

    def valid_arguments(self, name, meal_num, punish_type):
        if not name:
            raise JsonException(errcode=2001, errmsg="illege name")
        if len(name) > 20:
            raise JsonException(errcode=2002, errmsg="wrong name length")
        if meal_num < 0:
            raise JsonException(errcode=2003, errmsg="illege meal_num")
        if punish_type not in [0, 1, 2, 3, 4]:
            raise JsonException(errcode=2004, errmsg="illege punishtype")
