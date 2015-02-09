# -*- coding: utf-8 -*-

from tornado import gen
from tornado.httpclient import AsyncHTTPClient
from tornado.escape import json_encode, json_decode, url_escape

from config import API
from tools.auth import auth_login, auth_permission, no_monomer_hotel
from tools.url import add_get_params
from views.base import BtwBaseHandler
from exception.json_exception import JsonException
from exception.celery_exception import CeleryException

from constants import PERMISSIONS

from models.cooperate_hotel import CooperateHotelModel
from tasks.stock import PushHotelTask
from mixin.coop_mixin import CooperateMixin


class HotelCoopedAPIHandler(BtwBaseHandler):

    @gen.coroutine
    @auth_login(json=True)
    @auth_permission(PERMISSIONS.admin | PERMISSIONS.view_cooperated_hotel, json=True)
    def get(self):
        start = self.get_query_argument('start', 0)
        limit = self.get_query_argument('limit', 20)
        name = self.get_query_argument('name', None)
        city_id = self.get_query_argument('city_id', None)
        star = self.get_query_argument('star', None)
        is_online = self.get_query_argument('is_online', None)

        hotels, total = yield self.get_cooped_hotels(self.current_user.merchant_id, start, limit, name, city_id, star, is_online)
        if hotels is not None and total is not None:
            self.finish_json(result=dict(
                hotels=hotels,
                total=total,
                start=start,
                limit=limit,
                ))
        else:
            raise JsonException(500, 'query error')

    @gen.coroutine
    def get_cooped_hotels(self, merchant_id, start, limit, name, city_id, star, is_online):
        cooped_base_hotels = self.get_cooped_base_hotels(merchant_id, is_online)
        cooped_base_hotel_ids = [hotel.base_hotel_id for hotel in cooped_base_hotels]
        if not cooped_base_hotel_ids:
            raise gen.Return(([], 0))

        hotels, total = yield self.fetch_hotels(name, city_id, star, cooped_base_hotel_ids, start, limit)
        if hotels is not None and total is not None:
            yield self.merge_district(hotels)
            self.merge_base_hotel_with_coops(hotels, cooped_base_hotels)
            raise gen.Return((hotels, total))
        else:
            raise gen.Return((None, None))

    def get_cooped_base_hotels(self, merchant_id, is_online):
        return CooperateHotelModel.get_by_merchant_id(self.db, merchant_id, is_online)

    def merge_base_hotel_with_coops(self, base_hotels, cooped_hotels):
        for base in base_hotels:
            for cooped in cooped_hotels:
                if base['id'] == cooped.base_hotel_id:
                    base['base_hotel_id'] = base['id']
                    base['id'] = cooped.id
                    base['is_online'] = cooped.is_online
                    break

    @gen.coroutine
    def fetch_hotels(self, name, city_id, star, within_ids, start, limit):
        params = {'name': url_escape(name) if name else None, 'city_id': city_id, 'star': star, 'start': start, 'limit': limit}

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

    @gen.coroutine
    def merge_district(self, hotels):
        district_ids = [hotel['district_id'] for hotel in hotels]
        district_ids = {}.fromkeys(district_ids).keys()

        districts = yield self.fetch_districts(district_ids)

        for hotel in hotels:
            for district in districts:
                if hotel['district_id'] == district['id']:
                    hotel['district_name'] = district['name']
                    break
        raise gen.Return()

    @gen.coroutine
    def fetch_districts(self, district_ids):
        url = API['POI'] + '/api/district/?district_ids=' + url_escape(json_encode(district_ids))
        print url

        resp = yield AsyncHTTPClient().fetch(url)
        r = json_decode(resp.body)
        if r and r['errcode'] == 0:
            districts = r['result']['districts']
            raise gen.Return(districts)
        else:
            raise gen.Return([])

class HotelCoopOnlineAPIHandler(BtwBaseHandler):

    @auth_login(json=True)
    @auth_permission(PERMISSIONS.admin | PERMISSIONS.view_cooperated_hotel, json=True)
    def put(self, hotel_id, is_online):
        merchant_id = self.current_user.merchant_id
        is_online = int(is_online)
        if is_online not in [0, 1]:
            raise JsonException(errcode=500, errmsg="wrong arg: is_online")

        hotel = self.change_hotel_online_status(merchant_id, hotel_id, is_online)

        self.finish_json(result=dict(
            cooperate_hotel=hotel.todict()
            ))

    def change_hotel_online_status(self, merchant_id, hotel_id, is_online):
        hotel = CooperateHotelModel.get_by_merchant_id_and_hotel_id(self.db, merchant_id, hotel_id)
        if not hotel:
            raise JsonException(404, 'hotel not found')

        hotel.is_online = is_online
        self.db.commit()

        PushHotelTask().push_hotel.delay(hotel.id)
        return hotel

class HotelCoopedModifyAPIHandler(BtwBaseHandler, CooperateMixin):

    @auth_login(json=True)
    @no_monomer_hotel(json=True)
    @auth_permission(PERMISSIONS.admin | PERMISSIONS.choose_hotel, json=True)
    def delete(self, hotel_id):
        hotel = CooperateHotelModel.get_by_merchant_id_and_hotel_id(self.db, self.merchant.id, hotel_id)
        if not hotel:
            raise JsonException(1000, u'hotel not found')

        self.delete_hotel(hotel)

        self.finish_json(result=dict(
                hotel=hotel.todict()
            )
        )
