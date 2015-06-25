# -*- coding: utf-8 -*-

import json
import urllib
import datetime

from tornado import gen
from tornado.httpclient import AsyncHTTPClient
from models.rate_plan import RatePlanModel
from models.room_rate import RoomRateModel
from models.ota_channel import OtaChannelModel
from models.cooperate_hotel import CooperateHotelModel
from models.cooperate_roomtype import CooperateRoomTypeModel

from utils.stock_push import Pusher
from tools.json import json_encode

from exception.json_exception import JsonException

from tools.log import Log
from config import SPEC_STOCK_PUSH, API, IS_PUSH_TO_STOCK
from config import API, IS_PUSH_TO_STOCK
from constants import CHAIN_ID

class HotelPusher(Pusher):

    @gen.coroutine
    def push_hotel(self, hotel_id):
        Log.info("<<push hotel {}>> start".format(hotel_id))
        hotel = CooperateHotelModel.get_by_id(self.db, hotel_id, with_delete=True)
        if not hotel:
            Log.info("<<push hotel {}>> error hotel not exist".format(hotel_id))
            raise gen.Return(False)

        hotel_data = yield self.get_hotel_data(hotel)
        if hotel_data:
            r = yield self.post_hotel(hotel_data)
            raise gen.Return(r)
        else:
            raise gen.Return(False)



    @gen.coroutine
    def get_hotel_data(self, hotel):
        roomtypes = CooperateRoomTypeModel.get_by_hotel_id(self.db, hotel.id, with_delete=True)
        base_hotel, base_roomtypes = yield self.fetch_base_hotel_and_roomtypes(hotel.base_hotel_id)
        if not base_hotel:
            raise gen.Return(None)

        hotel_data = self.generate_hotel_data(hotel, roomtypes, base_hotel, base_roomtypes)
        raise gen.Return(hotel_data)


    @gen.coroutine
    def post_hotel(self, hotel_data):
        track_id = self.generate_track_id(hotel_data['id'])
        data = {'list': [hotel_data]}
        params = {'track_id': track_id, 'data': json.dumps(data)}
        Log.info(u"<<push hotel {}>> push data {}".format(hotel_data['id'], params))
        url = API['STOCK'] + '/stock/update_hotel?is_async=false'

        body = urllib.urlencode(params)

        if not IS_PUSH_TO_STOCK:
            raise gen.Return(True)

        try:
            r = yield AsyncHTTPClient().fetch(url, method='POST', body=body)
            resp = json.loads(r.body)
        except Exception, e:
            Log.exception(e)
            raise gen.Return(False)

        Log.info("<<push hotel {}>> response {}".format(hotel_data['id'], resp))
        if resp['errcode'] == 0:
            raise gen.Return(True)
        else:
            raise gen.Return(False)

    @gen.coroutine
    def fetch_base_hotel_and_roomtypes(self, hotel_id):
        url = API['POI'] + "/api/hotel/" + str(hotel_id) + "/roomtype/"
        try:
            r = yield AsyncHTTPClient().fetch(url)
            result = json.loads(r.body)
        except Exception, e:
            Log.exception(e)
            raise gen.Return((None, None))

        if result['errcode'] == 0:
            raise gen.Return((result['result']['hotel'], result['result']['roomtypes']))
        else:
            raise gen.Return((None, None))

    def generate_hotel_data(self, hotel, roomtypes, base_hotel, base_roomtypes):
        data = {}
        data['chain_id'] = CHAIN_ID
        data['id'] = hotel.id
        data['name'] = base_hotel['name']
        data['is_valid'] = self.cal_hotel_is_valid(hotel)
        data['city_id'] = base_hotel['city_id']
        data['district_id'] = base_hotel['district_id']
        data['address'] = base_hotel['address']
        data['star'] = base_hotel['star']
        data['tel'] = base_hotel['phone']
        data['facilities'] = base_hotel['facilities'].replace(',', '|') if base_hotel['facilities'] else ''
        data['room_types'] = self.generate_rooms(roomtypes, base_roomtypes)

        return data

    def generate_rooms(self, roomtypes, base_roomtypes):
        rooms = []
        for roomtype in roomtypes:
            for base_roomtype in base_roomtypes:
                if base_roomtype['id'] == roomtype.base_roomtype_id:
                    room = {}
                    room['id'] = roomtype.id
                    room['name'] = base_roomtype['name']
                    room['bed_type'] = base_roomtype['bed_type']
                    room['facilities'] = base_roomtype['facility'].replace(',', '|') if base_roomtype['facility'] else ''
                    room['is_valid'] = 1 if roomtype.is_delete == 0 else 0
                    rooms.append(room)
                    break
        return rooms

    def cal_hotel_is_valid(self, hotel):
        return 1 if hotel.is_suspend == 0 and hotel.is_online == 1 and hotel.is_delete == 0 else 0

