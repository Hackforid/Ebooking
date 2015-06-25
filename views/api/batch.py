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
from models.cooperate_roomtype import CooperateRoomTypeModel


class HotelRoomBatchAPIHandler(BtwBaseHandler):

    @gen.coroutine
    @auth_login(json=True)
    @auth_permission(PERMISSIONS.admin | PERMISSIONS.view_cooperated_hotel, json=True)
    def get(self):
        start = int(self.get_query_argument('start', 0))
        limit = int(self.get_query_argument('limit', 20))
        name = self.get_query_argument('name', None)
        city_id = self.get_query_argument('city_id', None)
        star = self.get_query_argument('star', None)
        city_id = int(city_id) if city_id is not None else None
        star = int(star) if star is not None else None

        hotels, total = yield self.get_cooped_hotels(self.merchant.id, name, city_id, star, start, limit)
        self.merge_roomtypes(hotels)

        self.finish_json(result=dict(
            hotels=hotels,
            total=total,
            start=start,
            limit=limit,
            ))


    @gen.coroutine
    def get_cooped_hotels(self, merchant_id, name, city_id, star, start, limit):
        cooped_hotels = CooperateHotelModel.get_by_merchant_id(self.db, merchant_id)
        cooped_hotels_base_ids =  [h.base_hotel_id for h in cooped_hotels]
        if not cooped_hotels_base_ids:
            raise gen.Return(([], 0))

        base_hotels, total = yield self.fetch_hotels_info(cooped_hotels_base_ids, name, city_id, star, start, limit)
        hotels = self.merge_hotel_info(cooped_hotels, base_hotels)

        raise gen.Return((hotels, total))

    @gen.coroutine
    def fetch_hotels_info(self, within_ids, name, city_id, star, start, limit):
        params = {'name': url_escape(name) if name else None, 'city_id': city_id, 'star': star, 'start': start, 'limit': limit, 'with_roomtype': 1}

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

    def merge_hotel_info(self, cooped_hotels, base_hotels):
        hotels = []
        for base_hotel in base_hotels:
            for cooped_hotel in cooped_hotels:
                if cooped_hotel.base_hotel_id == base_hotel['id']:
                    base_hotel['id'] = cooped_hotel.id
                    base_hotel['base_hotel_id'] = cooped_hotel.base_hotel_id
                    hotels.append(base_hotel)
                    break
        return hotels

    def merge_roomtypes(self, hotels):
        cooped_rooms = CooperateRoomTypeModel.get_by_merchant_id(self.db, self.merchant.id)
        cooped_rooms_base_ids = [room.base_roomtype_id for room in cooped_rooms]

        for hotel in hotels:
            _rooms = []
            for roomtype in hotel['roomtypes']:
                if roomtype['id'] in cooped_rooms_base_ids:
                    _rooms.append(roomtype)
            hotel['roomtypes'] = _rooms

        return hotels

class HotelRoomTypeOnlineAPIHandler(BtwBaseHandler):

    def post(self):
        pass
