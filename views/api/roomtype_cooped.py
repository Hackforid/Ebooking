# -*- coding: utf-8 -*-

import datetime
from dateutil.relativedelta import relativedelta

from tornado import gen
from tornado.httpclient import AsyncHTTPClient
from tornado.escape import json_encode, json_decode, url_escape

from config import API
from tools.auth import auth_login
from tools.url import add_get_params
from tools.request_tools import get_and_valid_arguments
from views.base import BtwBaseHandler
from exception.json_exception import JsonException

from tasks import celery_app
from tasks.models.cooperate_roomtype import CooperateRoomTypeModel as CooperateRoom
from tasks.models.cooperate_hotel import CooperateHotelModel
from tasks.models.inventory import InventoryModel

import tcelery
tcelery.setup_nonblocking_producer()

class RoomTypeCoopedAPIHandler(BtwBaseHandler):

    @gen.coroutine
    @auth_login(json=True)
    def get(self, hotel_id):
        m = int(self.get_query_argument('m', 0))
        simple = self.get_query_argument('simple', 0)
        year, month = self.get_inventory_month(m)

        hotel, roomtypes = yield self.get_all_roomtype(hotel_id)
        cooped_roomtypes = yield gen.Task(CooperateRoom.get_by_merchant_id_and_hotel_id.apply_async, args=[self.current_user.merchant_id, hotel_id])
        cooped, will_coop = self.seperate_roomtype(roomtypes, cooped_roomtypes.result)

        if not simple:
            inventorys = (yield gen.Task(InventoryModel.get_by_merchant_id_and_hotel_id_and_date.apply_async,
                args=[self.current_user.merchant_id, hotel_id, year, month])).result
            self.merge_inventory(cooped, inventorys)

        self.finish_json(result=dict(
            hotel=hotel,
            cooped_roomtypes=cooped,
            will_coop_roomtypes=will_coop,
            ))

    def merge_inventory(self, coop_rooms, inventorys):
        if not inventorys:
            return
        for room in coop_rooms:
            for inventory in inventorys:
                if room['id'] == inventory.roomtype_id:
                    room['inventory'] = inventory.todict()
                    break



    def get_inventory_month(self, m):
        if m < 0 or m > 2:
            raise JsonException(errcode=1003, errmsg="query date out of range")
        today = datetime.date.today()
        delta = relativedelta(months=m)
        day = today + delta
        return day.year, day.month


    @gen.coroutine
    def get_all_roomtype(self, hotel_id):
        resp = yield AsyncHTTPClient().fetch(API['POI'] + '/api/hotel/' + hotel_id + '/roomtype/')
        r = json_decode(resp.body)

        if r and r['errcode'] == 0:
            raise gen.Return((r['result']['hotel'], r['result']['roomtypes']))
        else:
            raise gen.Return((None, None))

    def seperate_roomtype(self, all_roomtypes, cooped_roomtypes):
        if cooped_roomtypes:
            cooped_roomtype_ids = [room.roomtype_id for room in cooped_roomtypes]
            print cooped_roomtype_ids
            cooped = [roomtype for roomtype in all_roomtypes if roomtype['id'] in cooped_roomtype_ids]
            will_coop = [roomtype for roomtype in all_roomtypes if roomtype['id'] not in cooped_roomtype_ids]
        else:
            cooped = []
            will_coop = all_roomtypes

        return cooped, will_coop

    
    @gen.coroutine
    @auth_login(json=True)
    def post(self, hotel_id):
        merchant_id = self.current_user.merchant_id
        args = self.get_json_arguments()
        roomtype_ids, = get_and_valid_arguments(args, 'roomtype_ids')

        if not roomtype_ids:
            raise JsonException(errcode=2001, errmsg="need id")

        hotel = (yield gen.Task(CooperateHotelModel.get_by_merchant_id_and_hotel_id.apply_async,
            args=[merchant_id, hotel_id])).result
        if not hotel:
            raise JsonException(errcode=404, errmsg="hotel not found")

        cooped_rooms = (yield gen.Task(CooperateRoom.get_by_merchant_id_and_hotel_id.apply_async,
            args=[merchant_id, hotel_id])).result
        if cooped_rooms:
            cooped_ids = [coop.id for coop in cooped_rooms]
            if set(cooped_ids) & set(roomtype_ids):
                raise JsonException(errcode=2001, errmsg="dunpile id")
        
        coops = (yield gen.Task(CooperateRoom.new_roomtype_coops.apply_async,
            args=[merchant_id, hotel_id, roomtype_ids])).result

        self.finish_json(result=dict(
            cooped_roomtypes=[coop.todict() for coop in coops],
            ))



        
