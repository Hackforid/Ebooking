# -*- coding: utf-8 -*-

from tornado import gen
from tornado.httpclient import AsyncHTTPClient
from tornado.escape import json_encode, json_decode, url_escape

from config import API
from tools.auth import auth_login, auth_permission, no_monomer_hotel
from tools.url import add_get_params
from views.base import BtwBaseHandler
from exception.json_exception import JsonException

from constants import PERMISSIONS
from models.cooperate_hotel import CooperateHotelModel

class HotelWillCoopAPIHandler(BtwBaseHandler):

    @gen.coroutine
    @auth_login(json=True)
    @no_monomer_hotel(json=True)
    @auth_permission(PERMISSIONS.admin | PERMISSIONS.choose_hotel, json=True)
    def get(self):
        start = self.get_query_argument('start', 0)
        limit = self.get_query_argument('limit', 20)
        name = self.get_query_argument('name', None)
        city_id = self.get_query_argument('city_id', None)
        star = self.get_query_argument('star', None)
        district_id = self.get_query_argument('district_id', None)

        hotels, total = yield self.get_will_coop_hotels(self.current_user.merchant_id, start, limit, name, city_id, district_id, star)
        if hotels is not None and total is not None:
            yield self.merge_district(hotels)
            self.finish_json(result=dict(
                hotels=hotels,
                total=total,
                start=start,
                limit=limit,
                ))
        else:
            raise JsonException(500, 'query error')

    @gen.coroutine
    def get_will_coop_hotels(self, merchant_id, start, limit, name, city_id, district_id, star):
        cooped_base_hotel_ids = self.get_cooped_base_hotel_ids(merchant_id)
        base_hotels, total = yield self.fetch_hotels(name, city_id, district_id, star, cooped_base_hotel_ids, start, limit)
        if base_hotels is not None and total is not None:
            raise gen.Return((base_hotels, total))
        else:
            raise gen.Return((None, None))

    def get_cooped_base_hotel_ids(self, merchant_id):
        hotels = CooperateHotelModel.get_by_merchant_id(self.db, merchant_id)
        return [hotel.base_hotel_id for hotel in hotels]

    @gen.coroutine
    def fetch_hotels(self, name, city_id, district_id, star, filter_ids, start, limit):
        params = {'name': url_escape(name) if name else None, 'city_id': city_id, 'district_id': district_id, 'star': star, 'start': start, 'limit': limit}

        if filter_ids:
            params['filter_ids'] = url_escape(json_encode(filter_ids))
        url = add_get_params(API['POI'] + u'/api/hotel/search/', params)

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
