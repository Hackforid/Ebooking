# -*- coding: utf-8 -*-

import time

from tornado import gen
from tornado.httpclient import AsyncHTTPClient
from tornado.escape import json_encode, json_decode, url_escape

from tools.auth import auth_login, auth_permission
from tools.request_tools import get_and_valid_arguments
from views.base import BtwBaseHandler
from exception.json_exception import JsonException
from exception.celery_exception import CeleryException

from tasks.stock import PushRatePlanTask

from constants import PERMISSIONS

from models.rate_plan import RatePlanModel
from models.room_rate import RoomRateModel
from models.cooperate_roomtype import CooperateRoomTypeModel


class RatePlanValidMixin(object):

    def valid_rateplan_arguments(self, name, meal_num, punish_type):
        self.valid_name(name)
        self.valid_meal_num(meal_num)
        self.valid_punish_type(punish_type)

    def valid_punish_type(self, punish_type):
        if punish_type not in [0, 1, 2, 3, 4]:
            raise JsonException(errcode=2003, errmsg="wrong punish_type")

    def valid_meal_num(self, meal_num):
        if meal_num not in [-1, 0, 1, 2, 100]:
            raise JsonException(errcode=2004, errmsg="wrong meal_num")

    def valid_name(self, name):
        if not isinstance(name, basestring):
            raise JsonException(errcode=2001, errmsg="wrong name")
        if len(name) > 20:
            raise JsonException(errcode=2002, errmsg="wrong name length")

    def valid_arrive_pay_args(self, guarantee_type, guarantee_start_time):
        self.valid_guarantee_type(guarantee_type)
        self.valid_gurantee_start_time(guarantee_start_time)

    def valid_guarantee_type(self, guarantee_type):
        if guarantee_type not in [0, 1, 2]:
            raise JsonException(errcode=2004, errmsg="wrong guarantee_type")

    def valid_gurantee_start_time(self, guarantee_start_time):
        try:
            time.strptime(guarantee_start_time, "%H:%M:%S")
        except ValueError as e:
            raise JsonException(errcode=2004, errmsg="wrong guarantee_time")

    def valid_pay_type(self, pay_type):
        if pay_type not in [0, 1]:
            raise JsonException(errcode=2004, errmsg="wrong pay_type")


class RatePlanAPIHandler(BtwBaseHandler, RatePlanValidMixin):

    @gen.coroutine
    @auth_login(json=True)
    @auth_permission(PERMISSIONS.admin | PERMISSIONS.pricing, json=True)
    def post(self, hotel_id, roomtype_id):
        args = self.get_json_arguments()
        merchant_id = self.current_user.merchant_id

        name, meal_num, punish_type = get_and_valid_arguments(
            args, 'name', 'meal_num', 'punish_type')
        pay_type = args.get('pay_type', RatePlanModel.PAY_TYPE_PRE)
        self.valid_pay_type(pay_type)
        self.valid_rateplan_arguments(name, meal_num, punish_type)

        if pay_type == RatePlanModel.PAY_TYPE_ARRIVE:
            guarantee_start_time, guarantee_type = get_and_valid_arguments(
                args, 'guarantee_start_time', 'guarantee_type')
            self.valid_arrive_pay_args(guarantee_type, guarantee_start_time)

            rateplan, roomrate = self.new_rate_plan(
                merchant_id, hotel_id, roomtype_id, name, meal_num, punish_type, pay_type, guarantee_type, guarantee_start_time)
        else:
            rateplan, roomrate = self.new_rate_plan(
                merchant_id, hotel_id, roomtype_id, name, meal_num, punish_type)

        self.finish_json(result=dict(
            rateplan=rateplan.todict(),
            roomrate=roomrate.todict(),
        ))

    @gen.coroutine
    @auth_login(json=True)
    @auth_permission(PERMISSIONS.admin | PERMISSIONS.pricing, json=True)
    def get(self, hotel_id, roomtype_id):
        merchant_id = self.current_user.merchant_id

        rateplans, roomrates = self.get_by_room(merchant_id, hotel_id, roomtype_id)

        self.finish_json(result=dict(
            rateplans=[rateplan.todict() for rateplan in rateplans],
            roomrates=[roomrate.todict() for roomrate in roomrates],
        ))

    def get_by_room(self, merchant_id, hotel_id, roomtype_id):
        rateplans = RatePlanModel.get_by_room(self.db, merchant_id, hotel_id, roomtype_id)
        rateplan_ids = [rateplan.id for rateplan in rateplans]
        roomrates= RoomRateModel.get_by_rateplans(self.db, rateplan_ids)
        return rateplans, roomrates


    def new_rate_plan(self, merchant_id, hotel_id, roomtype_id, name, meal_num, punish_type, pay_type=None, guarantee_type=None, guarantee_start_time=None):
        room = CooperateRoomTypeModel.get_by_id(self.db, roomtype_id)
        if not room:
            raise JsonException(errcode=404, errmsg='room not exist')

        rate_plan = RatePlanModel.get_by_merchant_hotel_room_name(
            self.db, merchant_id, hotel_id, roomtype_id, name)
        if rate_plan:
            raise CeleryException(errcode=405, errmsg="name exist")

        new_rateplan = RatePlanModel.new_rate_plan(self.db,
                                                   merchant_id, hotel_id, roomtype_id, room.base_hotel_id, room.base_roomtype_id,  name, meal_num, punish_type, pay_type, guarantee_type, guarantee_start_time)
        new_roomrate = RoomRateModel.new_roomrate(
            self.db, hotel_id, roomtype_id, room.base_hotel_id, room.base_roomtype_id, new_rateplan.id, meal_num)

        PushRatePlanTask().push_rateplan.delay(new_rateplan.id)
        return new_rateplan, new_roomrate


class RatePlanModifyAPIHandler(BtwBaseHandler, RatePlanValidMixin):

    @gen.coroutine
    @auth_login(json=True)
    @auth_permission(PERMISSIONS.admin | PERMISSIONS.pricing, json=True)
    def put(self, hotel_id, roomtype_id, rateplan_id):
        args = self.get_json_arguments()

        name = args.get("name", None)
        meal_num = args.get("meal_num", None)
        punish_type = args.get("punish_type", None)
        guarantee_type = args.get("guarantee_type", None)
        guarantee_start_time = args.get("guarantee_start_time", None)

        if name is not None:
            self.valid_name(name)
        if meal_num is not None:
            self.valid_meal_num(meal_num)
        if punish_type is not None:
            self.valid_punish_type(punish_type)
        if guarantee_type is not None:
            self.valid_guarantee_type(guarantee_type)
        if guarantee_start_time is not None:
            self.valid_gurantee_start_time(guarantee_start_time)


        rateplan, roomrate = self.modify_rateplan(
            rateplan_id, name, meal_num, punish_type, guarantee_type, guarantee_start_time)

        self.finish_json(result=dict(
            rateplan=rateplan.todict(),
            roomrate=roomrate.todict(),
        ))

    def modify_rateplan(self, rateplan_id, name, meal_num, punish_type, guarantee_type, guarantee_start_time):
        rateplan = RatePlanModel.get_by_id(self.db, rateplan_id)
        if not rateplan:
            return JsonException(errcode=404, errmsg="rateplan not found")

        if name is not None:
            _rateplan = RatePlanModel.get_by_merchant_hotel_room_name(self.db,
                                                                      rateplan.merchant_id, rateplan.hotel_id, rateplan.roomtype_id, name)
            if _rateplan and _rateplan.id != rateplan.id:
                return JsonException(errcode=405, errmsg="name exist")
            else:
                rateplan.name = name

        if meal_num is not None:
            roomrate = RoomRateModel.set_meal(
                self.db, rateplan.id, meal_num, False)
        if punish_type is not None:
            rateplan.punish_type = punish_type
        if rateplan.pay_type == rateplan.PAY_TYPE_ARRIVE:
            if guarantee_type is not None:
                rateplan.guarantee_type = guarantee_type
            if guarantee_start_time is not None:
                rateplan.guarantee_start_time = guarantee_start_time

        self.db.commit()

        PushRatePlanTask().push_rateplan.delay(rateplan.id, with_roomrate=True)
        return rateplan, roomrate
