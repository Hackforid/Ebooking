# -*- coding: utf-8 -*-

from tornado import gen
from tornado.httpclient import AsyncHTTPClient
from tornado.escape import json_encode, json_decode, url_escape

from config import API
from tools.auth import auth_login
from tools.url import add_get_params
from views.base import BtwBaseHandler
from models.cooperate_hotel import CooperateHotelModel as CooperateHotel
from exception.json_exception import JsonException

class HotelWillCoopAPIHandler(BtwBaseHandler):

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
        cooped_hotel_ids = self.get_cooped_hotel_ids(merchant_id)
        hotels, total = yield self.fetch_hotels(name, city_id, star, cooped_hotel_ids, start, limit)
        if hotels is not None and total is not None:
            raise gen.Return((hotels, total))
        else:
            raise gen.Return((None, None))

    def get_cooped_hotel_ids(self, merchant_id):
        cooped_hotels = CooperateHotel.get_by_merchant_id(self.db, merchant_id)
        return [hotel.hotel_id for hotel in cooped_hotels]

    @gen.coroutine
    def fetch_hotels(self, name, city_id, star, filter_ids, start, limit):
        params = {'name': url_escape(name) if name else None, 'city_id': city_id, 'star': star, 'start': start, 'limit': limit}

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
