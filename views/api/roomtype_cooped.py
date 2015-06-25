# -*- coding: utf-8 -*-

from datetime import datetime, timedelta

from tornado import gen
from tornado.httpclient import AsyncHTTPClient
from tornado.escape import json_encode, json_decode, url_escape

from config import API
from tools.auth import auth_login, auth_permission
from tools.request_tools import get_and_valid_arguments
from views.base import BtwBaseHandler
from exception.json_exception import JsonException

from mixin.coop_mixin import CooperateMixin

from constants import PERMISSIONS
from models.cooperate_hotel import CooperateHotelModel
from models.cooperate_roomtype import CooperateRoomTypeModel
from models.inventory import InventoryModel

from utils.stock_push.inventory import InventoryAsyncPusher
from utils.stock_push.hotel import HotelPusher
from utils.stock_push.poi import POIRoomTypePusher

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

        hotel = self.get_hotel(hotel_id)

        base_hotel, base_roomtypes = yield self.get_all_roomtype(hotel.base_hotel_id)
        cooped_roomtypes = self.get_cooped_rooms(hotel_id)

        base_cooped, base_will_coop = self.seperate_roomtype(base_roomtypes, cooped_roomtypes)
        self.valid_date(year, month)

        if not simple:
            inventorys = InventoryModel.get_by_merchant_id_and_hotel_id_and_date(self.db,
                    self.current_user.merchant_id, hotel_id, year, month)
            self.merge_inventory(base_cooped, inventorys)


        self.merge_cooped_info(base_cooped, cooped_roomtypes)

        self.finish_json(result=dict(
            hotel=base_hotel,
            cooped_roomtypes=base_cooped,
            will_coop_roomtypes=base_will_coop,
            ))

    def get_cooped_rooms(self, hotel_id):
        coops = CooperateRoomTypeModel.get_by_hotel_id(self.db, hotel_id)
        return coops

    def get_hotel(self, hotel_id):
        return CooperateHotelModel.get_by_id(self.db, hotel_id)

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
        max_date = today + timedelta(days=365)
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

        coops = yield self.new_roomtype_coops(merchant_id, hotel_id, roomtype_ids)
        self.finish_json(result=dict(
            cooped_roomtypes=[coop.todict() for coop in coops],
            ))

    @gen.coroutine
    def new_roomtype_coops(self, merchant_id, hotel_id, roomtype_ids):
        hotel = CooperateHotelModel.get_by_id(self.db, hotel_id)
        if not hotel:
            raise JsonException(1000, 'hotel not found')
        if hotel.merchant_id != merchant_id:
            raise JsonException(2000, 'merchant not valid')


        coops = CooperateRoomTypeModel.get_by_merchant_hotel_base_rooms_id(self.db,
                merchant_id, hotel_id, roomtype_ids)
        if coops:
            raise JsonException(1000, 'room has cooped')

        coops = CooperateRoomTypeModel.new_roomtype_coops(self.db,
                merchant_id, hotel.id,  hotel.base_hotel_id, roomtype_ids, commit=False)

        for coop in coops:
            InventoryModel.insert_in_months(self.db,
                    merchant_id, hotel_id, coop.id, hotel.base_hotel_id, coop.base_roomtype_id, 13, commit=False)

        r = yield HotelPusher(self.db).push_hotel_by_id(hotel_id)
        if not r:
            raise JsonException(3000, 'push hotel to stock fail')

        for coop in coops:
            r = yield InventoryAsyncPusher(self.db).push_by_roomtype(coop)
            if not r:
                raise JsonException(3001, 'push inventory to stock fail')

            r = yield POIRoomTypePusher(self.db).push_roomtype(coop.id)
            if not r:
                raise JsonException(3001, 'push roomtype to poi fail')

        self.db.commit()
        raise gen.Return(coops)



class RoomTypeCoopedModifyAPIHandler(BtwBaseHandler, CooperateMixin):

    @auth_login(json=True)
    @auth_permission(PERMISSIONS.admin | PERMISSIONS.inventory, json=True)
    def put(self, hotel_id, roomtype_id):
        merchant_id = self.current_user.merchant_id
        args = self.get_json_arguments()
        prefix_name, remark_name = get_and_valid_arguments(args,
                "prefix_name", "remark_name")


        room = self.modify_cooped_roomtype(merchant_id, hotel_id, roomtype_id, prefix_name, remark_name)
        self.finish_json(result=dict(
            cooped_roomtype=room.todict(),
            ))

    def modify_cooped_roomtype(self, merchant_id, hotel_id, roomtype_id, prefix_name, remark_name):
        coop = CooperateRoomTypeModel.get_by_id(self.db, roomtype_id)
        if not coop:
            return JsonException(404, 'coop not found')
        if coop.merchant_id != merchant_id:
            return JsonException(1000, 'merchant not valid')

        coop.prefix_name = prefix_name
        coop.remark_name = remark_name
        self.db.commit()
        return coop

    @gen.coroutine
    @auth_login(json=True)
    @auth_permission(PERMISSIONS.admin | PERMISSIONS.inventory, json=True)
    def delete(self, hotel_id, roomtype_id):
        room = CooperateRoomTypeModel.get_by_merchant_hotel_and_id(self.db, self.merchant.id, hotel_id, roomtype_id)
        if not room:
            raise JsonException(1001, 'roomtype not found')

        r = yield self.delete_roomtype(room)
        if r:
            self.db.commit()
            self.finish_json(result=dict(
                roomtype=room.todict()))
        else:
            self.db.rollback()
            raise JsonException(2000, 'delete fail')

class RoomTypeOnlineAPIHandler(BtwBaseHandler):

    @gen.coroutine
    def put(self, hotel_id, roomtype_id):

        args = self.get_json_arguments()
        is_online, = get_and_valid_arguments(args, 'is_online')
        if is_online not in [0, 1]:
            raise JsonException(errmsg='wrong arg is_online', errcode=2001)

        roomtype =  CooperateRoomTypeModel.get_by_merchant_hotel_and_id(self.db, self.merchant.id, hotel_id, roomtype_id)
        if not roomtype:
            raise JsonException(errmsg='roomtype not found', errcode=2002)

        roomtype.is_online = is_online
        self.db.flush()

        r = yield InventoryAsyncPusher(self.db).push_by_roomtype(roomtype)
        if r:
            self.db.commit()
            self.finish_json(result=dict(
                roomtype = roomtype.todict(),
                ))
        else:
            self.db.rollback()
            raise JsonException(1000, 'push stock fail')


class RoomTypeByMerchantOnlineAPIHandler(BtwBaseHandler):

    @gen.coroutine
    def put(self):

        args = self.get_json_arguments()
        is_online, = get_and_valid_arguments(args, 'is_online')
        if is_online not in [0, 1]:
            raise JsonException(errmsg='wrong arg is_online', errcode=2001)

        CooperateRoomTypeModel.set_online_by_merchant(self.db, self.merchant.id, is_online, commit=False)
        self.db.flush()

        r = yield InventoryAsyncPusher(self.db).push_inventory_by_merchant(self.merchant.id)
        if r:
            self.db.commit()
            self.finish_json()
        else:
            self.db.rollback()
            yield InventoryAsyncPusher(self.db).push_inventory_by_merchant(self.merchant.id)
            raise JsonException(1000, "push stock error")

