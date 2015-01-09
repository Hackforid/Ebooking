# -*- coding: utf-8 -*-

from datetime import datetime, timedelta

from tornado import gen
from tornado.httpclient import AsyncHTTPClient
from tornado.escape import json_encode, json_decode, url_escape

from config import API
from tools.auth import auth_login, auth_permission
from tools.url import add_get_params
from tools.request_tools import get_and_valid_arguments
from views.base import BtwBaseHandler
from exception.json_exception import JsonException
from exception.celery_exception import CeleryException

import tasks.models.cooperate_roomtype as CooperateRoom
from tasks.models import cooperate_hotel as CooperateHotel
import tasks.models.inventory as Inventory

from constants import PERMISSIONS

class RoomTypeCoopedAPIHandler(BtwBaseHandler):

    @gen.coroutine
    @auth_login(json=True)
    @auth_permission(PERMISSIONS.admin | PERMISSIONS.inventory, json=True)
    def get(self, hotel_id):
        today = datetime.today()
        year = self.get_query_argument('year', today.year)
        month = self.get_query_argument('month', today.month)
        year, month = int(year), int(month)
        simple = self.get_query_argument('simple', 0)

        hotel = yield self.get_hotel(hotel_id)

        base_hotel, base_roomtypes = yield self.get_all_roomtype(hotel.base_hotel_id)
        cooped_roomtypes = yield self.get_cooped_rooms(hotel_id)

        base_cooped, base_will_coop = self.seperate_roomtype(base_roomtypes, cooped_roomtypes)

        self.valid_date(year, month)

        if not simple:
            inventorys = (yield gen.Task(Inventory.get_by_merchant_id_and_hotel_id_and_date.apply_async,
                args=[self.current_user.merchant_id, hotel_id, year, month])).result
            self.merge_inventory(base_cooped, inventorys)

        self.merge_cooped_info(base_cooped, cooped_roomtypes)

        self.finish_json(result=dict(
            hotel=base_hotel,
            cooped_roomtypes=base_cooped,
            will_coop_roomtypes=base_will_coop,
            ))

    @gen.coroutine
    def get_cooped_rooms(self, hotel_id):
        task = yield gen.Task(CooperateRoom.get_by_hotel_id.apply_async, args=[hotel_id])
        if not task.result:
            raise gen.Return([])
        if task.status == 'SUCCESS':
            if task.result[0].merchant_id == self.current_user.merchant_id:
                raise gen.Return(task.result)
            else:
                raise JsonException(errorcode=1000, errmsg='merchant not valid')
        else:
            raise JsonException(errorcode=2001, errmsg='load room fail')

    @gen.coroutine
    def get_hotel(self, hotel_id):
        task = yield gen.Task(CooperateHotel.get_by_id.apply_async, args=[hotel_id])
        if task.status == 'SUCCESS':
            raise gen.Return(task.result)
        else:
            raise JsonException(errorcode=2000, errmsg='hotel not found')

    def merge_cooped_info(self, base_rooms, cooped_rooms):
        if not cooped_rooms:
            return
        for coop in cooped_rooms:
            for room in base_rooms:
                if room['id'] == coop.base_roomtype_id:
                    room['base_roomtype_id'] = room['id']
                    room['is_online'] = coop.is_online
                    room['cooped_roomtype_id'] = coop.id
                    room['prefix_name'] = coop.prefix_name
                    room['remark_name'] = coop.remark_name
                    break

    def merge_inventory(self, coop_rooms, inventorys):
        if not inventorys:
            return
        for room in coop_rooms:
            for inventory in inventorys:
                if room['id'] == inventory.base_roomtype_id:
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
        resp = yield AsyncHTTPClient().fetch(API['POI'] + '/api/hotel/' + str(hotel_id) + '/roomtype/')
        r = json_decode(resp.body)

        if r and r['errcode'] == 0:
            raise gen.Return((r['result']['hotel'], r['result']['roomtypes']))
        else:
            raise gen.Return((None, None))

    def seperate_roomtype(self, all_base_roomtypes, cooped_roomtypes):
        '''
        根据已合作room获取合作的和未合作的base_roomtype
        '''
        if cooped_roomtypes:
            cooped_roomtype_base_ids = [room.base_roomtype_id for room in cooped_roomtypes]
            cooped = [roomtype for roomtype in all_base_roomtypes if roomtype['id'] in cooped_roomtype_base_ids]
            will_coop = [roomtype for roomtype in all_base_roomtypes if roomtype['id'] not in cooped_roomtype_base_ids]
        else:
            cooped = []
            will_coop = all_base_roomtypes

        return cooped, will_coop

    @gen.coroutine
    @auth_login(json=True)
    @auth_permission(PERMISSIONS.admin | PERMISSIONS.inventory, json=True)
    def post(self, hotel_id):
        merchant_id = self.current_user.merchant_id
        args = self.get_json_arguments()
        roomtype_ids, = get_and_valid_arguments(args, 'roomtype_ids')

        if not roomtype_ids:
            raise JsonException(errcode=2001, errmsg="need id")

        task = yield gen.Task(CooperateRoom.new_roomtype_coops.apply_async,
            args=[merchant_id, hotel_id, roomtype_ids])
        if task.status == 'SUCCESS':
            self.finish_json(result=dict(
                cooped_roomtypes=[coop.todict() for coop in task.result],
                ))
        else:
            if isinstance(task.result, CeleryException):
                raise JsonException(errcode=1000, errmsg=task.result.errmsg)
            else:
                raise JsonException(errcode=2000, errmsg='server error')



class RoomTypeCoopedModifyAPIHandler(BtwBaseHandler):

    @gen.coroutine
    @auth_login(json=True)
    @auth_permission(PERMISSIONS.admin | PERMISSIONS.inventory, json=True)
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
