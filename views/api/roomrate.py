# -*- coding: utf-8 -*-

from datetime import datetime, timedelta, date

from tornado.escape import json_encode, json_decode, url_escape
from tornado import gen

from tools.auth import auth_login, auth_permission
from tools.request_tools import get_and_valid_arguments
from views.base import BtwBaseHandler
from exception.json_exception import JsonException

from constants import PERMISSIONS
from models.room_rate import RoomRateModel

from tools.log import Log
from utils.stock_push.rateplan import RoomRatePusher


class RoomRateAPIHandler(BtwBaseHandler):

    @gen.coroutine
    @auth_login(json=True)
    @auth_permission(PERMISSIONS.admin | PERMISSIONS.pricing, json=True)
    def put(self, hotel_id, roomtype_id, roomrate_id):
        args = self.get_json_arguments()
        Log.info(u"<<modify roomrate {}>> user:{} data: {}".format(roomrate_id, self.current_user.todict(), args))
        start_date, end_date, price = get_and_valid_arguments(args,
                'start_date', 'end_date', 'price')
        weekdays = args.get('weekdays', None)
        merchant_id = self.merchant.id

        self.valid_price(price)
        start_date, end_date = self.valid_date(start_date, end_date, weekdays)

        roomrate = yield self.set_price(merchant_id, roomrate_id, price, start_date, end_date, weekdays)
        self.finish_json(result=dict(
            roomrate=roomrate.todict(),
            ))



    def valid_date(self, str_start_date, str_end_date, weekdays):
        time_format = "%Y-%m-%d"
        try:
            start_date = datetime.strptime(str_start_date, time_format)
            end_date = datetime.strptime(str_end_date, time_format)
        except:
            raise JsonException(errcode=2001, errmsg="invalid date: date parse fail")

        if end_date < start_date:
            raise JsonException(errcode=2001, errmsg="invalid date: end date before start date")

        min_date = date.today()
        max_date = min_date + timedelta(days=365)

        if start_date.date() < min_date or start_date.date() >= max_date:
            raise JsonException(errcode=2001, errmsg="invalid date: start date out of range")

        if end_date.date() < min_date or end_date.date() >= max_date:
            raise JsonException(errcode=2001, errmsg="invalid date: end date out of range")

        if weekdays:
            if not set([1, 2, 3, 4, 5, 6, 7]).difference(weekdays):
                raise JsonException(errcode=2002, errmsg="invalid weekdays: end date out of range [1,2,3,4,5,6,7]")

        return start_date, end_date

    def valid_price(self, price):
        # range [0, 2^31]
        if not isinstance(price, int) or price < 0 or price > 999999:
            raise JsonException(errcode=2002, errmsg="price out of range")

    @gen.coroutine
    def set_price(self, merchant_id, roomrate_id, price, start_date, end_date, weekdays=None):
        roomrate = RoomRateModel.set_price(self.db, roomrate_id, price, start_date, end_date, weekdays, commit=False)
        if not roomrate:
            raise JsonException(1001, 'roomrate not found')
        self.db.flush()
        push_r = yield RoomRatePusher(self.db).push_roomrate(merchant_id, roomrate)
        if push_r:
            self.db.commit()
        else:
            raise JsonException(1002, 'push stock fail')
        raise gen.Return(roomrate)


class RoomRateTESTAPIHandler(RoomRateAPIHandler):

    @gen.coroutine
    def put(self):
        args = self.get_json_arguments()
        Log.info(u"<<modify roomrate>>  data: {}".format(args))
        merchant_id, roomrate_id, start_date, end_date, price = get_and_valid_arguments(args,
                'merchant_id', 'roomrate_id', 'start_date', 'end_date', 'price')
        weekdays = args.get('weekdays', None)

        self.valid_price(price)
        start_date, end_date = self.valid_date(start_date, end_date, weekdays)

        roomrate = yield self.set_price(merchant_id, roomrate_id, price, start_date, end_date, weekdays)
        self.finish_json(result=dict(
            roomrate=roomrate.todict(),
            ))

