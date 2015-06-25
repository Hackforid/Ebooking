# -*- coding: utf-8 -*-

import json
import urllib
import datetime

from tornado import gen
from tornado.httpclient import AsyncHTTPClient
from models.rate_plan import RatePlanModel
from models.room_rate import RoomRateModel
from models.ota_channel import OtaChannelModel

from utils.stock_push import Pusher
from tools.json import json_encode

from exception.json_exception import JsonException

from tools.log import Log
from config import SPEC_STOCK_PUSH, API, IS_PUSH_TO_STOCK
from constants import CHAIN_ID


class RatePlanPusher(Pusher):

    @gen.coroutine
    def push_by_id(self, rateplan_id, with_roomrate=True, with_cancel_rule=True):

        rateplan = RatePlanModel.get_by_id(self.db, rateplan_id, with_delete=True)
        roomrate = RoomRateModel.get_by_rateplan(self.db, rateplan_id, with_delete=True)
        if not rateplan or not roomrate:
            raise gen.Return()

        if not (yield self.post_rateplan(rateplan)):
            raise JsonException(1000, 'push rateplan fail')

        if with_cancel_rule:
            self.post_cancel_rule(rateplan)


    @gen.coroutine
    def post_rateplan(self, rateplan):

        rateplan_data = self.generate_rateplan_data(rateplan)

        track_id = self.generate_track_id(rateplan_data['rate_plan_id'])
        data = {'list': [rateplan_data]}
        params = {'track_id': track_id,
                'data': json_encode(data)
                }
        Log.info('push rateplan {} : {}'.format(rateplan.id, params))

        if not IS_PUSH_TO_STOCK:
            raise gen.Return(True)

        url = API['STOCK'] + '/stock/update_rate_plan?is_async=false'
        body = urllib.urlencode(params)
        r = yield AsyncHTTPClient().fetch(url, method="POST", body=body)
        resp = json.loads(r.body)
        Log.info("<<push rateplan {}>> response:{}".format(rateplan.id, resp))
        if resp and resp['errcode'] == 0:
            raise gen.Return(True)
        else:
            raise gen.Return(False)

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
        data['is_valid'] = self.cal_rateplan_isvalid(rateplan)
        data['start_date'] = rateplan.start_date
        data['end_date'] = rateplan.end_date
        return data

    def get_pay_type(self, rateplan):
        return 1 if rateplan.pay_type == 1 else 2

    def get_rate_type(self, rateplan):
        # 到付卖价0 预付底价 1
        return rateplan.pay_type

    @gen.coroutine
    def post_cancel_rule(self, rateplan):
        rateplan_data = self.generate_cancel_rule_data(rateplan)
        track_id = self.generate_track_id(rateplan.id)
        data = {'track_id': track_id, 'data': json_encode({'list': [rateplan_data]})}
        Log.info("<<push cancel rule rateplan {}>> data:{}".format(rateplan.id, data))
        if not IS_PUSH_TO_STOCK:
            raise gen.Return(True)

        url = API['STOCK'] + '/stock/update_cancel_rule?is_async=false'

        body = urllib.urlencode(data)
        r = yield AsyncHTTPClient().fetch(url, method="POST", body=body)
        resp = json.loads(r.body)
        Log.info("<<push cancel rateplan {}>> response:{}".format(rateplan.id, resp))
        if resp and resp['errcode'] == 0:
            raise gen.Return(True)
        else:
            raise gen.Return(False)

    def generate_cancel_rule_data(self, rateplan):
        data = {}
        data['chain_id'] = CHAIN_ID
        data['hotel_id'] = str(rateplan.hotel_id)
        data['room_type_id'] = str(rateplan.roomtype_id)
        data['rate_plan_id'] = str(rateplan.id)
        data['is_valid'] = self.cal_rateplan_isvalid(rateplan)

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

    def cal_rateplan_isvalid(self, rateplan):
        if rateplan.merchant_id in SPEC_STOCK_PUSH:
            return 0
        return 1 if rateplan.is_online == 1 and rateplan.is_delete == 0 else 0

    @gen.coroutine
    def update_rateplans_valid_status(self, rateplan_ids):
        Log.info("<< push rateplans {} update rateplan valid>>".format(rateplan_ids))
        if not IS_PUSH_TO_STOCK:
            raise gen.Return(True)

        rateplans = RatePlanModel.get_by_ids(self.db, rateplan_ids, with_delete=True)
        rateplan_datas = [{"chain_id": CHAIN_ID, "hotel_id": rateplan.hotel_id, "rate_plan_id": rateplan.id, "is_valid": self.cal_rateplan_isvalid(rateplan)} for rateplan in rateplans]

        track_id = self.generate_track_id(rateplan_ids)
        data = {'list': rateplan_datas, 'type': 3}
        params = {'track_id': track_id, 'data': json.dumps(data)}
        body = urllib.urlencode(params)
        url = API['STOCK'] + '/stock/update_state?is_async=false'

        Log.info("<< push rateplan {} update rateplan valid request {}>>".format(rateplan_ids, params))
        try:
            r = yield AsyncHTTPClient().fetch(url, method='POST', body=body)
            Log.info("<< push rateplan {} update rateplan valid response {}>>".format(rateplan_ids, r.body))
            resp = json.loads(r.body)
        except Exception, e:
            Log.exception(e)
            raise gen.Return(False)

        if resp['errcode'] == 0:
            raise gen.Return(True)
        else:
            raise gen.Return(False)

class RoomRatePusher(Pusher):

    @gen.coroutine
    def push_roomrate(self, merchant_id, roomrate):
        if (yield self.post_roomrate(merchant_id, roomrate)):
            raise gen.Return(True)
        else:
            raise gen.Return(False)

    @gen.coroutine
    def push_roomrate_by_rateplan(self, rateplan):
        roomrate = RoomRateModel.get_by_rateplan(self.db, rateplan.id, with_delete=True)
        r = yield self.push_roomrate(rateplan.merchant_id, roomrate)
        raise gen.Return(r)

    @gen.coroutine
    def post_roomrate(self, merchant_id, roomrate):
        roomrate_datas = self.generate_roomrate_datas(merchant_id, roomrate)
        track_id = self.generate_track_id(roomrate.id)
        data = {'track_id': track_id, 'data': json_encode({'list': roomrate_datas})}
        Log.info("<<push roomrate {}>>: {}".format(roomrate.id, data))

        if not IS_PUSH_TO_STOCK:
            raise gen.Return(True)

        url = API['STOCK'] + '/stock/update_room_rate?is_async=false'
        body = urllib.urlencode(data)
        r = yield AsyncHTTPClient().fetch(url, method="POST", body=body)
        resp = json.loads(r.body)
        Log.info("<<push roomrate {}>> response:{}".format(roomrate.id, r.body))
        if resp and resp['errcode'] == 0:
            raise gen.Return(True)
        else:
            raise gen.Return(False)

    def generate_roomrate_data(self, merchant_id, roomrate):
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

    def generate_roomrate_datas(self, merchant_id, roomrate):
        datas = []
        roomrate_data = self.generate_roomrate_data(merchant_id, roomrate)

        ota_channel = OtaChannelModel.get_by_hotel_id(self.db, roomrate.hotel_id)
        if ota_channel:
            ota_ids = ota_channel.get_ota_ids()
            for ota_id in ota_ids:
                data = roomrate_data.copy()
                data['ota_id'] = ota_id
                data['is_valid'] = 1
                datas.append(data)

        data0 = roomrate_data.copy()
        data0['ota_id'] = 0
        data0['is_valid'] = 0
        datas.append(data0)

        return datas
