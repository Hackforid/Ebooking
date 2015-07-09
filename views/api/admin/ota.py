# -*- coding: utf-8 -*-

from tornado.escape import json_encode, json_decode, url_escape
from tornado import gen
from tornado.httpclient import AsyncHTTPClient
from tornado.escape import json_encode, json_decode, url_escape

from exception.json_exception import JsonException

from tools.auth import auth_backstage_login, need_backstage_admin, need_backstage_ota
from tools.request_tools import get_and_valid_arguments
from tools.url import add_get_params
from tools.log import Log
from views.base import BackStageHandler

from models.cooperate_hotel import CooperateHotelModel
from models.ota_channel import OtaChannelModel

from utils.ota import (get_all_ota, change_ota)

from config import API


class OtaListAPIHandler(BackStageHandler):

    @gen.coroutine
    @auth_backstage_login(json=True)
    @need_backstage_admin(json=True)
    @need_backstage_ota(json=True)
    def get(self):
        url = '{}/hotelReader2/ota/getList'.format(API['OTA'])
        r = yield AsyncHTTPClient().fetch(url)
        self.finish(r.body)


class OtaHotelModifyAPIHandler(BackStageHandler):

    @gen.coroutine
    @auth_backstage_login(json=True)
    @need_backstage_admin(json=True)
    @need_backstage_ota(json=True)
    def put(self, hotel_id):
        Log.info(self.request.body)
        args = self.get_json_arguments()
        ota_ids, = get_and_valid_arguments(args, 'ota_ids')
        yield self.valid_ota_ids(ota_ids)

        ota_channel = OtaChannelModel.set_ota_ids(self.db, hotel_id, ota_ids, commit=False)
        r = yield change_ota(hotel_id, ota_ids)
        if not r:
            self.db.rollback()
            raise JsonException(1000, 'fail')
        else:
            self.db.commit()
            self.finish_json(result=dict(
                ota_channel=ota_channel.todict(),
                ))

    @gen.coroutine
    def valid_ota_ids(self, ota_ids):
        all_ota_ids = yield self.get_otas()
        if 0 in ota_ids:
            raise JsonException(1001, 'illeage ota ids')

        for id in ota_ids:
            if id not in all_ota_ids:
                raise JsonException(1001, 'illeage ota ids')

    @gen.coroutine
    def get_otas(self):
        otas = yield get_all_ota()
        ota_ids = [ota['id'] for ota in otas]
        ota_ids.append(13)
        raise gen.Return(ota_ids)


class OtaHotelOnlineAPIHandler(BackStageHandler):

    @gen.coroutine
    @auth_backstage_login(json=True)
    @need_backstage_admin(json=True)
    @need_backstage_ota(json=True)
    def put(self, ota_id, hotel_id, is_online):
        ota_id = int(ota_id)
        is_online = int(is_online)

        ota_ids = yield self.get_otas()
        if ota_id not in ota_ids:
            raise JsonException(1001, 'illeage ota ids')
        new_ota_ids = []
        if not ota_ids:
            raise JsonException(1000, 'get ota fail')

        ota_channel = OtaChannelModel.get_by_hotel_id(self.db, hotel_id)
        if not ota_channel:
            if is_online == 0:
                new_ota_ids = []
            else:
                new_ota_ids = [ota_id]
        else:
            if is_online == 0:
                if ota_id in ota_channel.get_ota_ids():
                    new_ota_ids = [id for id in ota_channel.get_ota_ids() if id != ota_id]
                else:
                    new_ota_ids = ota_channel.get_ota_ids()
            else:
                if ota_id not in ota_channel.get_ota_ids():
                    new_ota_ids = ota_channel.get_ota_ids()
                    new_ota_ids.append(ota_id)
                else:
                    new_ota_ids = ota_channel.get_ota_ids()

        ota_channel = OtaChannelModel.set_ota_ids(self.db, hotel_id, new_ota_ids, commit=False)

        r = yield change_ota(hotel_id, new_ota_ids)
        if not r:
            self.db.rollback()
            raise JsonException(1000, 'fail')
        else:
            self.db.commit()
            self.finish_json(result=dict(
                ota_channel=ota_channel.todict(),
                ))


    @gen.coroutine
    def get_otas(self):
        otas = yield get_all_ota()
        ota_ids = [ota['id'] for ota in otas]
        ota_ids.append(13)
        raise gen.Return(ota_ids)


class OtaHotelsAPIHandler(BackStageHandler):

    @gen.coroutine
    @auth_backstage_login(json=True)
    @need_backstage_admin(json=True)
    @need_backstage_ota(json=True)
    def get(self, ota_id):
        ota_id = int(ota_id)
        hotel_name = self.get_query_argument('hotel_name', None)
        merchant_id = self.get_query_argument('merchant_id', 1)
        city_id = self.get_query_argument('city_id', None)
        star = self.get_query_argument('star', None)
        district_id = self.get_query_argument('district_id', None)
        status = int(self.get_query_argument('status', 0))

        hotels, total = yield self.get_cooped_hotels(merchant_id, hotel_name, city_id, district_id, star, is_online=1)

        self.merge_ota(hotels)
        hotels = self.filter_by_ota_id(ota_id, hotels, status)

        self.finish_json(result=dict(
            hotels = hotels,
            ))

    def merge_ota(self, hotels):
        hotel_ids = [hotel['id'] for hotel in hotels]
        ota_channels = OtaChannelModel.get_by_hotel_ids(self.db, hotel_ids)

        for hotel in hotels:
            for ota_channel in ota_channels:
                if hotel['id'] == ota_channel.hotel_id:
                    hotel['ota_ids'] = ota_channel.get_ota_ids()
                    break
            else:
                hotel['ota_ids'] = []


    def filter_by_ota_id(self, ota_id, hotels, status):
        if status == 0:
            return hotels

        r = []
        for hotel in hotels:
            if ota_id in hotel['ota_ids']:
                if status == 1:
                    r.append(hotel)
            else:
                if status == 2:
                    r.append(hotel)
        return r

    @gen.coroutine
    def get_cooped_hotels(self, merchant_id, name, city_id, district_id, star, is_online):
        cooped_base_hotels = self.get_cooped_base_hotels(merchant_id, is_online)
        cooped_base_hotel_ids = [hotel.base_hotel_id for hotel in cooped_base_hotels]
        if not cooped_base_hotel_ids:
            raise gen.Return(([], 0))

        hotels, total = yield self.fetch_hotels(name, city_id, district_id, star, cooped_base_hotel_ids)
        if hotels is not None and total is not None:
            self.merge_base_hotel_with_coops(hotels, cooped_base_hotels)
            raise gen.Return((hotels, total))
        else:
            raise gen.Return((None, None))

    def get_cooped_base_hotels(self, merchant_id, is_online):
        return CooperateHotelModel.get_by_merchant_id(self.db, merchant_id, is_online)


    @gen.coroutine
    def fetch_hotels(self, name, city_id, district_id, star, within_ids):
        params = {'name': url_escape(name) if name else None, 'city_id': city_id, 'district_id': district_id, 'star': star, 'start': 0, 'limit': 65536}

        if within_ids:
            params['within_ids'] = url_escape(json_encode(within_ids))
        url = add_get_params(API['POI'] + u'/api/hotel/search/', params)

        resp = yield AsyncHTTPClient().fetch(url)

        r = json_decode(resp.body)

        if r and r['errcode'] == 0:
            hotels = r['result']['hotels']
            total = r['result']['total']
            raise gen.Return((hotels, total))
        else:
            raise gen.Return((None, None))

    def merge_base_hotel_with_coops(self, base_hotels, cooped_hotels):
        for base in base_hotels:
            for cooped in cooped_hotels:
                if base['id'] == cooped.base_hotel_id:
                    base['base_hotel_id'] = base['id']
                    base['id'] = cooped.id
                    base['is_online'] = cooped.is_online
                    break


