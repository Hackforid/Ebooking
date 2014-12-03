# -*- coding: utf-8 -*-

from tornado.escape import json_encode, json_decode, url_escape

from tools.auth import auth_login
from views.base import BtwBaseHandler
from models.cooperate_hotel import CooperateHotelModel as CooperateHotel
from exception.json_exception import JsonException

class HotelCoopAPIHandler(BtwBaseHandler):

    @auth_login(json=True)
    def post(self, hotel_id):
        merchant_id = self.current_user.merchant_id
        coop = CooperateHotel.get_by_merchant_id_and_hotel_id(self.db, merchant_id, hotel_id)

        if coop:
            raise JsonException(1000, "已经合作")
        else:
            coop = CooperateHotel.new_hotel_cooprate(self.db, merchant_id, hotel_id)

        self.finish_json(result=dict(
            hotel_cooprate=coop.todict(),
            ))



