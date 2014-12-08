# -*- coding: utf-8 -*-

from tornado.escape import json_encode, json_decode, url_escape
from tornado import gen

from tools.auth import auth_login
from views.base import BtwBaseHandler
from tasks.models.cooperate_hotel import CooperateHotelModel as CooperateHotel
from exception.json_exception import JsonException

class HotelCoopAPIHandler(BtwBaseHandler):

    @gen.coroutine
    @auth_login(json=True)
    def post(self, hotel_id):
        merchant_id = self.current_user.merchant_id
        coop_task = yield gen.Task(CooperateHotel.get_by_merchant_id_and_hotel_id.apply_async, args=[merchant_id, hotel_id])
        coop = coop_task.result

        if coop:
            raise JsonException(1000, "已经合作")
        else:
            coop_task = yield gen.Task(CooperateHotel.new_hotel_cooprate.apply_async, args=[merchant_id, hotel_id])
            coop = coop_task.result

        self.finish_json(result=dict(
            hotel_cooprate=coop.todict(),
            ))



