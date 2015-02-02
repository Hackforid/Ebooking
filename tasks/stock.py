# -*- coding: utf-8 -*-

import json
import time
import datetime

from celery.contrib.methods import task_method
from celery import chain

from tasks.celery_app import app
from tasks.base_task import SqlAlchemyTask

from exception.celery_exception import CeleryException
from tools.json import json_encode
from config import API, IS_PUSH_TO_STOCK
from constants import QUEUE_STOCK_PUSH, CHAIN_ID
from tools.net import req

class PushHotelTask(SqlAlchemyTask):

    LEN_HOTEL = 40

    @app.task(filter=task_method, ignore_result=True, queue=QUEUE_STOCK_PUSH)
    def push_hotel_suspend_by_merchant_id(self, merchant_id):
        self.log.info("<<push hotel by merchant {}>> start".format(merchant_id))
        from models.cooperate_hotel import CooperateHotelModel
        hotels = CooperateHotelModel.get_by_merchant_id(self.session, merchant_id)
        hotel_list = [{'chain_id': CHAIN_ID, "hotel_id": hotel.id, "is_valid": self.cal_hotel_is_valid(hotel)} for hotel in hotels]

        self.post_hotels(merchant_id, hotel_list)

    def cal_hotel_is_valid(self, hotel):
        return 1 if hotel.is_suspend == 0 and hotel.is_online == 1 else 0

    def post_hotels(self, merchant_id, hotel_list):
        if not IS_PUSH_TO_STOCK:
            return
        track_id = self.generate_track_id(merchant_id)
        data = {'list': hotel_list, 'type': 1}
        params = {'track_id': track_id, 'data': json.dumps(data)}
        self.log.info(u"<<push hotel by merchant {}>> push data {}".format(merchant_id, params))
        url = API['STOCK'] + '/stock/update_state'
        r = req.post(url, data=params)
        self.log.info("<<push hotel by merchant {}>> response {}".format(merchant_id, r.text))

    @app.task(filter=task_method, queue=QUEUE_STOCK_PUSH)
    def push_all_hotels(self):
        if not IS_PUSH_TO_STOCK:
            return

        from models.merchant import MerchantModel
        merchants = MerchantModel.get_all(self.session)
        for merchant in merchants:
            self.log.info("=== push merchant {} ===".format(merchant.id))
            self.push_by_merchant(merchant)

    def push_by_merchant(self, merchant):
        from models.cooperate_hotel import CooperateHotelModel as Hotel
        hotels = Hotel.get_by_merchant_id(self.session, merchant.id)
        hotel_datas = [self.get_hotel_data(hotel) for hotel in hotels]
        hotel_data_list = [hotel_datas[i : i+self.LEN_HOTEL] for i in range(0, len(hotel_datas), self.LEN_HOTEL)] 
        for hotel_datas in hotel_data_list:
            self.post_hotels(hotel_datas)


    @app.task(filter=task_method, ignore_result=True, queue=QUEUE_STOCK_PUSH)
    def push_hotel(self, hotel_id):
        self.log.info("<<push hotel {}>> start".format(hotel_id))
        from models.cooperate_hotel import CooperateHotelModel
        hotel = CooperateHotelModel.get_by_id(self.session, hotel_id)
        if not hotel:
            return

        hotel_data = self.get_hotel_data(hotel)
        self.post_hotel(hotel_data)

    def get_hotel_data(self, hotel):
        from models.cooperate_roomtype import CooperateRoomTypeModel
        roomtypes = CooperateRoomTypeModel.get_by_hotel_id(self.session, hotel.id)
        base_hotel, base_roomtypes = self.fetch_base_hotel_and_roomtypes(hotel.base_hotel_id)
        if not base_hotel:
            return

        hotel_data = self.generate_hotel_data(hotel, roomtypes, base_hotel, base_roomtypes)
        return hotel_data


    def post_hotel(self, hotel_data):
        if not IS_PUSH_TO_STOCK:
            return
        track_id = self.generate_track_id(hotel_data['id'])
        data = {'list': [hotel_data]}
        params = {'track_id': track_id, 'data': json.dumps(data)}
        self.log.info(u"<<push hotel {}>> push data {}".format(hotel_data['id'], params))
        url = API['STOCK'] + '/stock/update_hotel'
        r = req.post(url, data=params)
        self.log.info("<<push hotel {}>> response {}".format(hotel_data['id'], r.text))

    def post_hotels(self, hotel_datas):
        if not IS_PUSH_TO_STOCK:
            return
        if not hotel_datas:
            return
        track_id = self.generate_track_id()
        data = {'list': hotel_datas}
        params = {'track_id': track_id, 'data': json.dumps(data)}
        self.log.info(u"<<push hotels>> push data {}".format(params))
        url = API['STOCK'] + '/stock/update_hotel'
        r = req.post(url, data=params)
        self.log.info("<<push hotels>> response {}".format(r.text))

    def generate_track_id(self, hotel_id=0):
        return "{}|{}".format(hotel_id, time.time())

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
                    room['is_valid'] = roomtype.is_online
                    rooms.append(room)
                    break
        return rooms

    def fetch_base_hotel_and_roomtypes(self, hotel_id):
        url = API['POI'] + "/api/hotel/" + str(hotel_id) + "/roomtype/"
        r = req.get(url)
        if r.status_code == 200:
            result = r.json()
            if result['errcode'] == 0:
                return result['result']['hotel'], result['result']['roomtypes']

        return None, None

class PushRatePlanTask(SqlAlchemyTask):

    MAX_PUSH_NUM = 40

    @app.task(filter=task_method, queue=QUEUE_STOCK_PUSH)
    def push_all_rateplan_cancelrule_roomrate(self):
        from models.merchant import MerchantModel
        merchants = MerchantModel.get_all(self.session)
        for merchant in merchants:
            self.push_by_merchant(merchant)

    def push_by_merchant(self, merchant):
        from models.rate_plan import RatePlanModel

        rateplans = RatePlanModel.get_by_merchant(self.session, merchant.id)
        rateplan_datas = [self.generate_rateplan_data(rateplan) for rateplan in rateplans]
        cancel_rule_datas =  [self.generate_cancel_rule_data(rateplan) for rateplan in rateplans]

        rateplan_data_list = [rateplan_datas[i: i+self.MAX_PUSH_NUM] for i in range(0, len(rateplan_datas), self.MAX_PUSH_NUM)]
        cancel_rule_list = [cancel_rule_datas[i: i+self.MAX_PUSH_NUM] for i in range(0, len(cancel_rule_datas), self.MAX_PUSH_NUM)]

        for rateplan_data in rateplan_data_list:
            self.post_rateplans(rateplan_data)
        for cancel_rule_data in cancel_rule_list:
            self.post_cancel_rules(cancel_rule_data)

        self.push_roomrate_by_rateplans(rateplans)


    def push_roomrate_by_rateplans(self, rateplans):
        from models.room_rate import RoomRateModel
        
        rateplan_ids = [rateplan.id for rateplan in rateplans]

        roomrates= RoomRateModel.get_by_rateplans(self.session, rateplan_ids)
        roomrate_datas = [self.generate_roomrate_data(roomrate) for roomrate in roomrates] 
        roomrate_data_list = [roomrate_datas[i: i+self.MAX_PUSH_NUM] for i in range(0, len(roomrate_datas), self.MAX_PUSH_NUM)]
        for roomrate_data in roomrate_data_list:
            self.post_roomrates(roomrate_data)

    @app.task(filter=task_method, ignore_result=True, queue=QUEUE_STOCK_PUSH)
    def push_rateplan(self, rateplan_id, with_cancel_rule=True, with_roomrate=True):
        self.log.info("<< push rateplan {}>>".format(rateplan_id))
        from models.rate_plan import RatePlanModel
        from models.room_rate import RoomRateModel

        rateplan = RatePlanModel.get_by_id(self.session, rateplan_id)
        roomrate = RoomRateModel.get_by_rateplan(self.session, rateplan_id)
        if not rateplan or not roomrate:
            self.log.info('not found')
            return

        self.post_rateplan(rateplan)

        if with_cancel_rule:
            self.post_cancel_rule(rateplan)

        if with_roomrate:
            self.post_roomrate(roomrate)


    def post_rateplan(self, rateplan):
        if not IS_PUSH_TO_STOCK:
            return
        rateplan_data = self.generate_rateplan_data(rateplan)

        track_id = self.generate_track_id(rateplan_data['rate_plan_id'])
        data = {'list': [rateplan_data]}
        params = {'track_id': track_id,
                'data': json_encode(data)
                }
        self.log.info(params)
        url = API['STOCK'] + '/stock/update_rate_plan'
        r = req.post(url, data=params)
        self.log.info(r.text)

    def post_rateplans(self, rateplan_data):
        if not IS_PUSH_TO_STOCK:
            return

        track_id = self.generate_track_id(0)
        data = {'list': rateplan_data}
        params = {'track_id': track_id,
                'data': json_encode(data)
                }
        self.log.info(params)
        url = API['STOCK'] + '/stock/update_rate_plan'
        r = req.post(url, data=params)
        self.log.info(r.text)

    def post_cancel_rule(self, rateplan):
        if not IS_PUSH_TO_STOCK:
            return
        rateplan_data = self.generate_cancel_rule_data(rateplan)
        track_id = self.generate_track_id(rateplan.id)
        data = {'track_id': track_id, 'data': json_encode({'list': [rateplan_data]})}
        self.log.info("<<push rateplan {}>> data:{}".format(rateplan.id, data))

        url = API['STOCK'] + '/stock/update_cancel_rule'
        r = req.post(url, data)
        self.log.info("<<push rateplan {}>> response:{}".format(rateplan.id, r.text))

    def post_cancel_rules(self, cancel_rule_data):
        if not IS_PUSH_TO_STOCK:
            return
        track_id = self.generate_track_id(1)
        data = {'track_id': track_id, 'data': json_encode({'list': cancel_rule_data})}

        self.log.info("<<push cancel rules>> request: {}".format(data))
        url = API['STOCK'] + '/stock/update_cancel_rule'
        r = req.post(url, data)
        self.log.info("<<push cancel rules>> response: {}".format(r.text))

    def post_roomrate(self, roomrate):
        if not IS_PUSH_TO_STOCK:
            return
        roomrate_data = self.generate_roomrate_data(roomrate)
        track_id = self.generate_track_id(roomrate.id)
        data = {'track_id': track_id, 'data': json_encode({'list': [roomrate_data]})}
        self.log.info(data)

        url = API['STOCK'] + '/stock/update_room_rate'
        r = req.post(url, data)
        self.log.info(r.text)

    def post_roomrates(self, roomrate_data):
        if not IS_PUSH_TO_STOCK:
            return
        track_id = self.generate_track_id(2)
        data = {'track_id': track_id, 'data': json_encode({'list': roomrate_data})}
        self.log.info("push roomrates {}".format(data))

        url = API['STOCK'] + '/stock/update_room_rate'
        r = req.post(url, data)
        self.log.info("push roomrates resp {}".format(r.text))


    def generate_track_id(self, rateplan_id):
        return "{}|{}".format(rateplan_id, time.time())

    def generate_rateplan_data(self, rateplan):
        data = {}
        data['chain_id'] = CHAIN_ID
        data['hotel_id'] = rateplan.hotel_id
        data['rate_plan_id'] = rateplan.id
        data['name'] = rateplan.name
        data['rate_type'] = self.get_rate_type(rateplan)
        data['pay_type'] = self.get_pay_type(rateplan)
        data['stay_days'] = rateplan.stay_days
        data['ahead_days'] = rateplan.ahead_days
        data['guarantee_start_time'] = rateplan.guarantee_start_time
        data['guarantee_type'] = rateplan.guarantee_type
        data['guarantee_count'] = rateplan.guarantee_count
        data['is_valid'] = rateplan.is_online
        data['start_date'] = rateplan.start_date
        data['end_date'] = rateplan.end_date
        return data

    def get_rate_type(self, rateplan):
        return rateplan.pay_type

    def get_pay_type(self, rateplan):
        return 1 if rateplan.pay_type == 1 else 2

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
        rule['cancel_type'] = 2 # 罚款取消
        rule['punish_type'] = rateplan.punish_type
        rule['punish_value'] = rateplan.punish_value
        rule['start_date'] = rateplan.start_date
        rule['end_date'] = rateplan.end_date
        rule['desc'] = ''

        data['rule_array'] = [rule]

        return data

    def generate_roomrate_data(self, roomrate):
        data = {}
        data['chain_id'] = CHAIN_ID
        data['hotel_id'] = str(roomrate.hotel_id)
        data['room_type_id'] = str(roomrate.roomtype_id)
        data['rate_plan_id'] = str(roomrate.rate_plan_id)

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

    MAX_PUSH_NUM = 40

    @app.task(filter=task_method, queue=QUEUE_STOCK_PUSH)
    def push_all_inventories(self):
        from models.merchant import MerchantModel
        start_day = datetime.date.today()
        days = [start_day + datetime.timedelta(days=i) for i in xrange(90)]
        days = [(day.year, day.month) for day in days]
        days = {}.fromkeys(days).keys()
        merchants = MerchantModel.get_all(self.session)
        for merchant in merchants:
            self.push_by_merchant_in_days(merchant, days)


    def push_by_merchant_in_days(self, merchant, days):
        self.log.info(">> push inventories by merchant {}".format(merchant.id))

        from models.inventory import InventoryModel
        inventories = InventoryModel.get_by_merchant_and_dates(self.session, merchant.id, days)
        inventory_list = [inventories[i: i+self.MAX_PUSH_NUM] for i in range(0, len(inventories), self.MAX_PUSH_NUM)]
        for inventories in inventory_list:
            self.post_inventory(inventories)


    @app.task(filter=task_method, ignore_result=True, queue=QUEUE_STOCK_PUSH)
    def push_inventory(self, roomtype_id):
        self.log.info("<< push inventory (roomtype {})>>".format(roomtype_id))
        from models.inventory import InventoryModel

        start_day = datetime.date.today()
        days = [start_day + datetime.timedelta(days=i) for i in xrange(90)]
        days = [(day.year, day.month) for day in days]
        days = {}.fromkeys(days).keys()

        inventories = InventoryModel.get_by_roomtype_and_dates(self.session, roomtype_id, days)
        self.post_inventory(inventories)

    def post_inventory(self, inventories):
        if not IS_PUSH_TO_STOCK:
            return
        if not inventories:
            self.log.info('no inventoris')
            return
        inventory_data = self.generate_inventory_data(inventories)
        track_id = generate_track_id(inventories[0].roomtype_id)

        params = {'track_id': track_id,
                'data': json_encode({'list': [inventory_data]})}
        self.log.info(params)

        url = API['STOCK'] + '/stock/update_inventory'

        r = req.post(url, data=params)
        self.log.info(r.text)


    def generate_inventory_data(self, inventories):
        start_day = datetime.date.today()
        end_day = start_day + datetime.timedelta(days=89)

        manual_confirm_count = []

        day = start_day
        while day <= end_day:
            month = int("{}{:0>2d}".format(day.year, day.month))
            for inventory in inventories:
                if inventory.month == month:
                    manual_confirm_count.append(str(inventory.get_day(day.day)))
                    break
            day = day + datetime.timedelta(days=1)

        data = {}
        data['chain_id'] = CHAIN_ID
        data['ota_id'] = 0
        data['hotel_id'] = str(inventories[0].hotel_id)
        data['room_type_id'] = str(inventories[0].roomtype_id)
        data['manual_confirm_counts'] = '|'.join(manual_confirm_count)
        data['start_date'] = start_day
        data['end_date'] = end_day
        data['is_soldout_auto_close'] = 1

        return data


def generate_track_id(key):
    return "{}|{}".format(key, time.time())


@app.task(ignore_result=True, queue=QUEUE_STOCK_PUSH)
def push_all_to_stock():
    PushHotelTask().push_all_hotels.delay().get()
    PushRatePlanTask().push_all_rateplan_cancelrule_roomrate.delay().get()
    PushInventoryTask().push_all_inventories.delay().get()
