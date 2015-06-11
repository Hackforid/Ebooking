# -*- coding: utf-8 -*-

import json
import urllib
import datetime

import requests

from tornado import gen
from tornado.httpclient import AsyncHTTPClient

from models.rate_plan import RatePlanModel
from models.room_rate import RoomRateModel
from models.inventory import InventoryModel
from models.cooperate_roomtype import CooperateRoomTypeModel

from utils.stock_push import Pusher
from tools.json import json_encode
from tools.net import req


from tools.log import Log
from config import SPEC_STOCK_PUSH, API, IS_PUSH_TO_STOCK
from constants import CHAIN_ID

class InventoryPusher(Pusher):
    '''
    Push in celery task
    '''

    def push_by_roomtype_id(self, roomtype_id):

        roomtype = CooperateRoomTypeModel.get_by_id(self.db, roomtype_id)
        if not roomtype:
            return True

        start_day = datetime.date.today()
        days = [start_day + datetime.timedelta(days=i) for i in xrange(90)]
        days = [(day.year, day.month) for day in days]
        days = {}.fromkeys(days).keys()

        inventories = InventoryModel.get_by_roomtype_and_dates(self.db, roomtype_id, days)
        return self.post_inventory(inventories, roomtype.is_online)

    def post_inventory(self, inventories, is_online=1):
        if not inventories:
            return True
        inventory_data = self.generate_inventory_data(inventories, is_online)
        track_id = self.generate_track_id(inventories[0].roomtype_id)

        params = {'track_id': track_id,
                'data': json_encode({'list': [inventory_data]})}

        Log.info("push inventory roomtype {}: {}".format(inventories[0].roomtype_id, params))
        if not IS_PUSH_TO_STOCK:
            return True

        url = API['STOCK'] + '/stock/update_inventory?is_async=false'
        r = requests.post(url, data=params)
        Log.info("push inventory roomtype {} response {}".format(inventories[0].roomtype_id, r.text))

        return r.status_code == 200 and r.json()['errcode'] == 0



    def generate_inventory_data(self, inventories, is_online=1):
        start_day = datetime.date.today()
        end_day = start_day + datetime.timedelta(days=89)

        manual_confirm_count = []
        if is_online == 1:
            day = start_day
            while day <= end_day:
                month = int("{}{:0>2d}".format(day.year, day.month))
                for inventory in inventories:
                    if inventory.month == month:
                        manual_confirm_count.append(str(inventory.get_day(day.day)))
                        break
                day = day + datetime.timedelta(days=1)
        else:
            manual_confirm_count = '0' * 90

        data = {}
        data['chain_id'] = CHAIN_ID

        if inventories[0].merchant_id in SPEC_STOCK_PUSH:
            data['ota_id'] = SPEC_STOCK_PUSH[inventories[0].merchant_id]
        else:
            data['ota_id'] = 0

        data['hotel_id'] = str(inventories[0].hotel_id)
        data['room_type_id'] = str(inventories[0].roomtype_id)
        data['manual_confirm_counts'] = '|'.join(manual_confirm_count)
        data['start_date'] = start_day
        data['end_date'] = end_day
        data['is_soldout_auto_close'] = 1

        return data

class InventoryAsyncPusher(InventoryPusher):

    @gen.coroutine
    def push_inventory_by_merchant(self, merchant_id):
        Log.info(">> push inventories by merchant {}".format(merchant_id))
        roomtypes = CooperateRoomTypeModel.get_by_merchant_id(self.db, merchant_id)

        for roomtype in roomtypes:
            r = yield self.push_by_roomtype(roomtype)
            if not r:
                raise gen.Return(False)
        raise gen.Return(True)

    @gen.coroutine
    def push_by_roomtype_id(self, roomtype_id):
        roomtype = CooperateRoomTypeModel.get_by_id(self.db, roomtype_id)
        r = yield self.push_by_roomtype(roomtype)
        raise gen.Return(r)


    @gen.coroutine
    def push_by_roomtype(self, roomtype):
        start_day = datetime.date.today()
        days = [start_day + datetime.timedelta(days=i) for i in xrange(90)]
        days = [(day.year, day.month) for day in days]
        days = {}.fromkeys(days).keys()

        inventories = InventoryModel.get_by_roomtype_and_dates(self.db, roomtype.id, days)
        r = yield self.post_inventory(inventories, roomtype.is_online)
        raise gen.Return(r)

    @gen.coroutine
    def post_inventory(self, inventories, is_online=1):
        if not inventories:
            raise gen.Return(False)
        inventory_data = self.generate_inventory_data(inventories, is_online)
        track_id = self.generate_track_id(inventories[0].roomtype_id)

        params = {'track_id': track_id,
                'data': json_encode({'list': [inventory_data]})}

        Log.info("push inventory roomtype {}: {}".format(inventories[0].roomtype_id, params))
        if not IS_PUSH_TO_STOCK:
            raise gen.Return(True)

        url = API['STOCK'] + '/stock/update_inventory?is_async=false'
        r = yield AsyncHTTPClient().fetch(url, method='POST',
                body=urllib.urlencode(params))

        Log.info("push inventory roomtype {} response {}".format(inventories[0].roomtype_id, r.body))
        resp = json.loads(r.body)

        raise gen.Return(resp and resp['errcode'] == 0)
