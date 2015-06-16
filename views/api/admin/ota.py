# -*- coding: utf-8 -*-

from tornado.escape import json_encode, json_decode, url_escape
from tornado import gen
from tornado.httpclient import AsyncHTTPClient
from tornado.escape import json_encode, json_decode, url_escape

from exception.json_exception import JsonException

from tools.auth import auth_backstage_login, need_backstage_admin
from tools.request_tools import get_and_valid_arguments
from tools.url import add_get_params
from views.base import BackStageHandler

from models.cooperate_hotel import CooperateHotelModel
from models.ota_channel import OtaChannelModel

from config import API


class OtaListAPIHandler(BackStageHandler):

    @gen.coroutine
    @auth_backstage_login(json=True)
    @need_backstage_admin(json=True)
    def get(self):
        url = '{}/hotelReader2/ota/getList'.format(API['OTA'])
        r = yield AsyncHTTPClient().fetch(url)
        self.finish(r.body)


class OtaHotelsAPIHandler(BackStageHandler):

    @gen.coroutine
    @auth_backstage_login(json=True)
    @need_backstage_admin(json=True)
    def get(self, ota_id):
        ota_id = int(ota_id)
        hotel_name = self.get_query_argument('hotel_name', None)
        merchant_id = self.get_query_argument('merchant_id', 1)
        city_id = self.get_query_argument('city_id', None)
        star = self.get_query_argument('star', None)
        district_id = self.get_query_argument('district_id', None)
        status = int(self.get_query_argument('status', 0))

        hotels, total = yield self.get_cooped_hotels(merchant_id, hotel_name, city_id, district_id, star, is_online=1)

        hotels = self.filter_by_ota_id(ota_id, hotels)

        self.finish_json(result=dict(
            hotels = hotels,
            ))

    def filter_by_ota_id(self, ota_id, hotels):
        hotel_ids = [hotel['id'] for hotel in hotels]
        ota_channels = OtaChannelModel.get_by_hotel_ids(self.db, hotel_ids)

        r = []
        for hotel in hotels:
            for ota_channel in ota_channels:
                if hotel['id'] == ota_channel.hotel_id:
                    ota_ids = ota_channel.get_ota_ids()
                    if ota_id in ota_ids:
                        r.append(hotel)
                        break
                    else:
                        break
            else:
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
        print 'url=', url

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
