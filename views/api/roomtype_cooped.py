# -*- coding: utf-8 -*-

from datetime import datetime, timedelta

from tornado import gen
from tornado.httpclient import AsyncHTTPClient
from tornado.escape import json_encode, json_decode, url_escape

from config import API
from tools.auth import auth_login
from tools.url import add_get_params
from tools.request_tools import get_and_valid_arguments
from views.base import BtwBaseHandler
from exception.json_exception import JsonException
from exception.celery_exception import CeleryException

import tasks.models.cooperate_roomtype as CooperateRoom
import tasks.models.cooperate_hotel as CooperateHotelModel
import tasks.models.inventory as Inventory

import tcelery
tcelery.setup_nonblocking_producer()

class RoomTypeCoopedAPIHandler(BtwBaseHandler):

    @gen.coroutine
    @auth_login(json=True)
    def get(self, hotel_id):
        today = datetime.today()
        year = self.get_query_argument('year', today.year)
        month = self.get_query_argument('month', today.month)
        year, month = int(year), int(month)
        simple = self.get_query_argument('simple', 0)


        hotel, roomtypes = yield self.get_all_roomtype(hotel_id)
        cooped_roomtypes = yield gen.Task(CooperateRoom.get_by_merchant_id_and_hotel_id.apply_async, args=[self.current_user.merchant_id, hotel_id])
        cooped, will_coop = self.seperate_roomtype(roomtypes, cooped_roomtypes.result)

        self.valid_date(year, month)
        if not simple:
            inventorys = (yield gen.Task(Inventory.get_by_merchant_id_and_hotel_id_and_date.apply_async,
                args=[self.current_user.merchant_id, hotel_id, year, month])).result
            self.merge_inventory(cooped, inventorys)

        self.merge_cooped_info(cooped, cooped_roomtypes.result)

        self.finish_json(result=dict(
            hotel=hotel,
            cooped_roomtypes=cooped,
            will_coop_roomtypes=will_coop,
            ))

    def merge_cooped_info(self, rooms, coops):
        for coop in coops:
            for room in rooms:
                if room['id'] == coop.roomtype_id:
                    room['is_online'] = coop.is_online
                    room['coop_id'] = coop.id
                    room['prefix_name'] = coop.prefix_name
                    room['remark_name'] = coop.remark_name
                    break

    def merge_inventory(self, coop_rooms, inventorys):
        if not inventorys:
            return
        for room in coop_rooms:
            for inventory in inventorys:
                if room['id'] == inventory.roomtype_id:
                    room['inventory'] = inventory.todict()
                    break



    def valid_date(self, year, month):
        date = datetime(year, month, 1)
        today = datetime.today()

        min_date = datetime(today.year, today.month, 1)
        max_date = min_date + timedelta(days=90)
        if date < min_date or date > max_date:
            raise JsonException(errcode=1003, errmsg="query date out of range")


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


class RoomTypeCoopedModifyAPIHandler(BtwBaseHandler):

    @gen.coroutine
    @auth_login(json=True)
    def put(self, hotel_id, roomtype_id):
        merchant_id = self.current_user.merchant_id
        args = self.get_json_arguments()
        prefix_name, remark_name = get_and_valid_arguments(args,
                "prefix_name", "remark_name")


        task = yield gen.Task(CooperateRoom.modify_cooped_roomtype.apply_async,
                args=[merchant_id, hotel_id, roomtype_id, prefix_name, remark_name])
        result = task.result
        if isinstance(result, CeleryException):
            raise JsonException(errcode=1002, errmsg=result.errmsg)
        else:
            self.finish_json(result=dict(
                cooped_roomtype=result.todict(),
                ))
