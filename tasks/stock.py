# -*- coding: utf-8 -*-

import requests
import json
import time
import datetime

from celery.contrib.methods import task_method

from tasks.celery_app import app
from tasks.base_task import SqlAlchemyTask

from exception.celery_exception import CeleryException
from tools.json import json_encode
from config import CHAIN_ID, API

class PushHotelTask(SqlAlchemyTask):

    @app.task(filter=task_method, ignore_result=True)
    def push_hotel(self, hotel_id):
        from models.cooperate_hotel import CooperateHotelModel
        from models.cooperate_roomtype import CooperateRoomTypeModel

        hotel = CooperateHotelModel.get_by_id(self.session, hotel_id)
        if not hotel:
            return

        roomtypes = CooperateRoomTypeModel.get_by_hotel_id(self.session, hotel_id)

        base_hotel, base_roomtypes = self.fetch_base_hotel_and_roomtypes(hotel.base_hotel_id)
        if not base_hotel:
            return

        hotel_data = self.generate_data(hotel, roomtypes, base_hotel, base_roomtypes)
        self.post_hotel(hotel_data)

    def post_hotel(self, hotel_data):
        track_id = self.generate_track_id(hotel_data['id'])
        data = {'list': [hotel_data]}
        params = {'track_id': track_id, 'data': json.dumps(data)}
        print params
        url = API['STOCK'] + '/stock/update_hotel'
        r = requests.post(url, data=params)
        print r.text

    def generate_track_id(self, hotel_id):
        return "{}|{}".format(hotel_id, time.time())

    def fetch_base_hotel(self, base_hotel_id):
        url = API['POI'] + "/api/hotel/" + str(base_hotel_id)
        r = requests.get(url)
        if r.status_code == 200:
            result = r.json()
            if result['errorcode'] == 0:
                return result['result']['hotel']

    def generate_data(self, hotel, roomtypes, base_hotel, base_roomtypes):
        data = {}
        data['chain_id'] = CHAIN_ID
        data['id'] = hotel.id
        data['name'] = base_hotel['name']
        data['is_valid'] = hotel.is_online
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
                    room['is_valid'] = roomtype.is_online
                    rooms.append(room)
                    break
        return rooms



    def fetch_base_hotel_and_roomtypes(self, hotel_id):
        url = API['POI'] + "/api/hotel/" + str(hotel_id) + "/roomtype/"
        r = requests.get(url)
        if r.status_code == 200:
            result = r.json()
            if result['errcode'] == 0:
                return result['result']['hotel'], result['result']['roomtypes']

        return None, None

class PushRatePlanTask(SqlAlchemyTask):

    @app.task(filter=task_method, ignore_result=True)
    def push_rateplan(self, rateplan_id, with_cancel_rule=True, with_roomrate=True):
        from models.rate_plan import RatePlanModel
        from models.room_rate import RoomRateModel

        rateplan = RatePlanModel.get_by_id(self.session, rateplan_id)
        roomrate = RoomRateModel.get_by_rateplan(self.session, rateplan_id)
        if not rateplan or not roomrate:
            print 'not found'
            return

        self.post_rateplan(rateplan, roomrate)

        if with_cancel_rule:
            self.post_cancel_rule(rateplan)

        if with_roomrate:
            self.post_roomrate(rateplan, roomrate)


    def post_rateplan(self, rateplan, roomrate):
        rateplan_data = self.generate_rateplan_date(rateplan, roomrate)

        track_id = self.generate_track_id(rateplan_data['rate_plan_id'])
        data = {'list': [rateplan_data]}
        params = {'track_id': track_id,
                'data': json_encode(data)
                }
        print params
        url = API['STOCK'] + '/stock/update_rate_plan'
        r = requests.post(url, data=params)
        print r.text

    def post_cancel_rule(self, rateplan):
        rateplan_data = self.generate_cancel_rule_data(rateplan)
        track_id = self.generate_track_id(rateplan.id)
        data = {'track_id': track_id, 'data': json_encode({'list': [rateplan_data]})}
        print data

        url = API['STOCK'] + '/stock/update_cancel_rule'
        r = requests.post(url, data)
        print r.text

    def post_roomrate(self, rateplan, roomrate):
        roomrate_data = self.generate_roomrate_data(rateplan, roomrate)
        track_id = self.generate_track_id(rateplan.id)
        data = {'track_id': track_id, 'data': json_encode({'list': [roomrate_data]})}
        print data

        url = API['STOCK'] + '/stock/update_room_rate'
        r = requests.post(url, data)
        print r.text



    def generate_track_id(self, rateplan_id):
        return "{}|{}".format(rateplan_id, time.time())

    def generate_rateplan_date(self, rateplan, roomrate):
        data = {}
        data['chain_id'] = CHAIN_ID
        data['hotel_id'] = rateplan.hotel_id
        data['rate_plan_id'] = rateplan.id
        data['name'] = rateplan.name
        data['rate_type'] = 0
        data['pay_type'] = rateplan.pay_type
        data['stay_days'] = rateplan.stay_days
        data['ahead_days'] = rateplan.ahead_days
        data['guarantee_start_time'] = rateplan.guarantee_start_time
        data['guarantee_type'] = rateplan.guarantee_type
        data['guarantee_count'] = rateplan.guarantee_count
        data['breakfast'] = roomrate.get_meal()
        data['is_valid'] = rateplan.is_online
        data['start_date'] = rateplan.start_date
        data['end_date'] = rateplan.end_date
        return data

    def generate_cancel_rule_data(self, rateplan):
        data = {}
        data['chain_id'] = CHAIN_ID
        data['hotel_id'] = str(rateplan.hotel_id)
        data['room_type_id'] = str(rateplan.roomtype_id)
        data['rate_plan_id'] = str(rateplan.id)
        data['is_valid'] = rateplan.is_online

        rule = {}
        rule['cancel_days'] = rateplan.cancel_days
        rule['cancel_time'] = 0
        rule['cancel_type'] = rateplan.cancel_type
        rule['punish_type'] = rateplan.punish_type
        rule['punish_value'] = rateplan.punish_value
        rule['start_date'] = rateplan.start_date
        rule['end_date'] = rateplan.end_date
        rule['desc'] = ''

        data['rule_array'] = [rule]

        return data

    def generate_roomrate_data(self, rateplan, roomrate):
        data = {}
        data['chain_id'] = CHAIN_ID
        data['hotel_id'] = str(rateplan.hotel_id)
        data['room_type_id'] = str(rateplan.roomtype_id)
        data['rate_plan_id'] = str(rateplan.id)
        data['pay_type'] = rateplan.pay_type

        data['instant_confirm'] = '|'.join([str(0) for i in xrange(90)])
        meal_num = roomrate.get_meal()
        data['meals'] = '|'.join([str(meal_num) for i in xrange(90)])
        
        data['start_date'] = datetime.date.today() 
        data['end_date'] = data['start_date'] + datetime.timedelta(days=89) 

        day = datetime.date.today()
        days = [day + datetime.timedelta(days=i) for i in xrange(90)]
        data['prices'] = '|'.join([str(roomrate.get_price_by_date(d.month, d.day)) for d in days])

        return data


class PushInventoryTask(SqlAlchemyTask):

    @app.task(filter=task_method, ignore_result=True)
    def push_inventory(self, roomtype_id):
        from models.inventory import InventoryModel

        start_day = datetime.date.today()
        days = [start_day + datetime.timedelta(days=i) for i in xrange(90)]
        days = [(day.year, day.month) for day in days]
        days = {}.fromkeys(days).keys()

        print '==' * 20
        print roomtype_id, days
        inventories = InventoryModel.get_by_roomtype_and_dates(self.session, roomtype_id, days)
        self.post_inventory(inventories)

    def post_inventory(self, inventories):
        if not inventories:
            print 'no inventoris'
            return
        inventory_data = self.generate_inventory_data(inventories)
        track_id = generate_track_id(inventories[0].roomtype_id)

        params = {'track_id': track_id,
                'data': json_encode({'list': [inventory_data]})}
        print params

        url = API['STOCK'] + '/stock/update_inventory'

        r = requests.post(url, data=params)
        print r.text


    def generate_inventory_data(self, inventories):
        start_day = datetime.date.today()
        end_day = start_day + datetime.timedelta(days=89)

        auto_confirm_count = []
        manual_confirm_count = []

        day = start_day
        while day <= end_day:
            month = int("{}{:0>2d}".format(day.year, day.month))
            for inventory in inventories:
                if inventory.month == month:
                    auto, manual = inventory.get_day_count(day.day)
                    auto_confirm_count.append(str(auto))
                    manual_confirm_count.append(str(manual))
                    break
            day = day + datetime.timedelta(days=1)

        data = {}
        data['chain_id'] = CHAIN_ID
        data['ota_id'] = 0
        data['hotel_id'] = str(inventories[0].hotel_id)
        data['room_type_id'] = str(inventories[0].roomtype_id)
        data['auto_confirm_counts'] = '|'.join(auto_confirm_count)
        data['manual_confirm_counts'] = '|'.join(manual_confirm_count)
        data['start_date'] = start_day
        data['end_date'] = end_day
        data['is_soldout_auto_close'] = 1

        return data


def generate_track_id(key):
    return "{}|{}".format(key, time.time())
