# -*- coding: utf-8 -*-

from tornado.escape import json_encode, json_decode, url_escape
from tornado import gen

from tools.auth import auth_login
from views.base import BtwBaseHandler
import tasks.models.cooperate_hotel as CooperateHotel
from exception.json_exception import JsonException
from exception.celery_exception import CeleryException

class HotelCoopAPIHandler(BtwBaseHandler):

    @gen.coroutine
    @auth_login(json=True)
    def post(self, hotel_id):
        merchant_id = self.current_user.merchant_id
        coop_task = yield gen.Task(CooperateHotel.new_hotel_cooprate.apply_async, args=[merchant_id, hotel_id])
        if coop_task.status == 'SUCCESS':
            self.finish_json(result=dict(
                hotel_cooprate=coop_task.result.todict(),
                ))
        else:
            if isinstance(coop_task.result, CeleryException):
                raise JsonException(errcode=1000, errmsg=coop_task.result.errmsg)
            else:
                raise JsonException(errcode=2000, errmsg='server error')




