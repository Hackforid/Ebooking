# -*- coding: utf-8 -*-

from tornado.escape import json_encode, json_decode, url_escape
from tornado import gen

from tools.auth import auth_login, auth_permission, no_monomer_hotel
from tools.request_tools import get_and_valid_arguments
from views.base import BtwBaseHandler
from exception.json_exception import JsonException
from constants import PERMISSIONS
from tasks.poi import POIPushHotelTask
from models.cooperate_hotel import CooperateHotelModel
from mixin.coop_mixin import CooperateMixin
from utils.stock_push.hotel import HotelPusher
from utils.stock_push.poi import POIHotelPusher

class HotelCoopAPIHandler(BtwBaseHandler, CooperateMixin):

    @gen.coroutine
    @auth_login(json=True)
    @no_monomer_hotel(json=True)
    @auth_permission(PERMISSIONS.admin | PERMISSIONS.choose_hotel, json=True)
    def post(self, hotel_id):
        merchant_id = self.current_user.merchant_id
        hotel = yield self.new_hotel_cooprate(merchant_id, hotel_id)
        self.finish_json(result=dict(
            hotel_cooprate=hotel.todict(),
            ))

    @gen.coroutine
    def new_hotel_cooprate(self, merchant_id, hotel_id):
        coop = CooperateHotelModel.get_by_merchant_id_and_base_hotel_id(self.db, merchant_id, hotel_id, with_delete=True)
        if coop and coop.is_delete == 0:
            raise JsonException(1000, u'已经合作')

        if not coop:
            coop = CooperateHotelModel.new_hotel_cooprate(self.db, merchant_id, hotel_id)
        else:
            coop.is_delete = 0
            self.db.flush()

        r = yield HotelPusher(self.db).push_hotel(coop)
        if not r:
            raise JsonException(2000, 'push hotel to stock fail')

        r = yield POIHotelPusher(self.db).push_hotel(coop.id)
        if not r:
            raise JsonException(2000, 'push hotel to poi fail')

        self.db.commit()
        raise gen.Return(coop)


class HotelCoopsAPIHandler(BtwBaseHandler):

    @gen.coroutine
    @auth_login(json=True)
    @no_monomer_hotel(json=True)
    @auth_permission(PERMISSIONS.admin | PERMISSIONS.choose_hotel, json=True)
    def post(self):
        merchant_id = self.current_user.merchant_id
        args = self.get_json_arguments()
        hotel_ids, = get_and_valid_arguments(args, 'hotel_ids')
        coops = yield self.new_hotel_cooprates(merchant_id, hotel_ids)
        self.finish_json(result=dict(
            hotel_cooprate=[coop.todict() for coop in coops], 
            ))

    @gen.coroutine
    def new_hotel_cooprates(self, merchant_id, hotel_ids):
        coops = CooperateHotelModel.new_hotel_cooprates(self.db, merchant_id, hotel_ids, commit=False)
        hotel_pusher = HotelPusher(self.db)
        r = yield hotel_pusher.push_hotels(coops)
        if not r:
            self.db.rollback()
            raise JsonException(1000, 'push hotel to stock fail')
        else:
            self.db.commit()

        raise gen.Return(coops)


