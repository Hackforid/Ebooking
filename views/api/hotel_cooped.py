# -*- coding: utf-8 -*-

from tornado import gen
from tornado.httpclient import AsyncHTTPClient
from tornado.escape import json_encode, json_decode, url_escape

from config import API
from tools.auth import auth_login
from tools.url import add_get_params
from views.base import BtwBaseHandler
from exception.json_exception import JsonException

from tasks import celery_app
from tasks.models.cooperate_hotel import CooperateHotelModel as CooperateHotel

import tcelery
tcelery.setup_nonblocking_producer()

class HotelCoopedAPIHandler(BtwBaseHandler):

    @gen.coroutine
    @auth_login(json=True)
    def get(self):
        start = self.get_query_argument('start', 0)
        limit = self.get_query_argument('limit', 20)
        name = self.get_query_argument('name', None)
        city_id = self.get_query_argument('city_id', None)
        star = self.get_query_argument('star', None)

        hotels, total = yield self.get_will_coop_hotels(self.current_user.merchant_id, start, limit, name, city_id, star)
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
    def get_will_coop_hotels(self, merchant_id, start, limit, name, city_id, star):
        cooped_hotel_ids = yield self.get_cooped_hotel_ids(merchant_id)
        hotels, total = yield self.fetch_hotels(name, city_id, star, cooped_hotel_ids, start, limit)
        if hotels is not None and total is not None:
            yield self.mege_district(hotels)
            raise gen.Return((hotels, total))
        else:
            raise gen.Return((None, None))

    @gen.coroutine
    def get_cooped_hotel_ids(self, merchant_id):
        cooped_hotels = yield gen.Task(CooperateHotel.get_by_merchant_id.apply_async, args=[merchant_id])
        raise gen.Return([hotel.hotel_id for hotel in cooped_hotels.result])

    @gen.coroutine
    def fetch_hotels(self, name, city_id, star, within_ids, start, limit):
        params = {'name': url_escape(name) if name else None, 'city_id': city_id, 'star': star, 'start': start, 'limit': limit}

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

    @gen.coroutine
    def mege_district(self, hotels):
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

