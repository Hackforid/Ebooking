# -*- coding: utf-8 -*-

from tornado.escape import json_encode, json_decode, url_escape

from tools.auth import auth_login, auth_permission, no_monomer_hotel
from tools.request_tools import get_and_valid_arguments
from views.base import BtwBaseHandler
from exception.json_exception import JsonException
from constants import PERMISSIONS
from tasks.stock import PushHotelTask
from tasks.poi import POIPushHotelTask
from models.cooperate_hotel import CooperateHotelModel

class HotelCoopAPIHandler(BtwBaseHandler):

    @auth_login(json=True)
    @no_monomer_hotel(json=True)
    @auth_permission(PERMISSIONS.admin | PERMISSIONS.choose_hotel, json=True)
    def post(self, hotel_id):
        merchant_id = self.current_user.merchant_id
        hotel = self.new_hotel_cooprate(merchant_id, hotel_id)
        self.finish_json(result=dict(
            hotel_cooprate=hotel.todict(),
            ))

    def new_hotel_cooprate(self, merchant_id, hotel_id):
        coop = CooperateHotelModel.get_by_merchant_id_and_base_hotel_id(self.db, merchant_id, hotel_id)
        if coop:
            raise JsonException(1000, u'已经合作')

        coop = CooperateHotelModel.new_hotel_cooprate(self.db, merchant_id, hotel_id)

        PushHotelTask().push_hotel.delay(coop.id)
        POIPushHotelTask().push_hotel.delay(coop.id)

        return coop



class HotelCoopsAPIHandler(BtwBaseHandler):

    @auth_login(json=True)
    @no_monomer_hotel(json=True)
    @auth_permission(PERMISSIONS.admin | PERMISSIONS.choose_hotel, json=True)
    def post(self):
        merchant_id = self.current_user.merchant_id
        args = self.get_json_arguments()
        hotel_ids, = get_and_valid_arguments(args, 'hotel_ids')
        coops = self.new_hotel_cooprates(merchant_id, hotel_ids)
        self.finish_json(result=dict(
            hotel_cooprate=[coop.todict() for coop in coops], 
            ))

    def new_hotel_cooprates(self, merchant_id, hotel_ids):
        coops = CooperateHotelModel.new_hotel_cooprates(self.db, merchant_id, hotel_ids)
        for coop in coops:
            POIPushHotelTask().push_hotel.delay(coop.id)
        return coops


