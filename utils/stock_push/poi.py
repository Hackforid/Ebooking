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
from config import API, IS_PUSH_TO_POI

class POIRoomTypePusher(Pusher):

    @gen.coroutine
    def push_roomtype(self, roomtype_id):
        Log.info("<<POI push room mapping {}>> start".format(roomtype_id))

        room = CooperateRoomTypeModel.get_by_id(self.db, roomtype_id)
        if not room:
            Log.error("<<POI push room mapping {}>> no roomtype".format(roomtype_id))
            raise gen.Return(False)

        room_data = self.generate_data(room)
        r = yield self.post_room(room_data)
        raise gen.Return(r)

    def generate_data(self, room):
        data = {}
        data['chain_hotel_id'] = room.hotel_id
        data['chain_roomtype_id'] = room.id
        data['main_roomtype_id'] = room.base_roomtype_id
        return data

    @gen.coroutine
    def post_room(self, room_data):
        Log.info(u"<<POI push roomtype mapping>> push request {}".format(room_data))
        url = API['POI'] + '/api/push/ebooking/room/'
        body = json.dumps(room_data)
        if not IS_PUSH_TO_POI:
            raise gen.Return(True)
        try:
            r = yield AsyncHTTPClient().fetch(url, method='POST', headers={"Content-Type": "application/json"}, body=body)
            Log.info("<<POI push roomtype mapping>> response {}".format(r.body))
            resp = json.loads(r.body)
        except Exception, e:
            Log.exception(e)
            raise gen.Return(False)
        if resp['errcode'] == 0:
            raise gen.Return(True)
        else:
            raise gen.Return(False)
