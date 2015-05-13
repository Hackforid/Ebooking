# -*- coding: utf-8 -*-

from datetime import datetime, timedelta, date

from tornado.escape import json_encode, json_decode, url_escape

from tools.auth import auth_login, auth_permission
from tools.request_tools import get_and_valid_arguments
from views.base import BtwBaseHandler
from exception.json_exception import JsonException

from constants import PERMISSIONS
from models.room_rate import RoomRateModel
from tasks.stock import PushRatePlanTask

from tools.log import Log

class RoomRateAPIHandler(BtwBaseHandler):

    @auth_login(json=True)
    @auth_permission(PERMISSIONS.admin | PERMISSIONS.pricing, json=True)
    def put(self, hotel_id, roomtype_id, roomrate_id):
        args = self.get_json_arguments()
        Log.info(u"modify roomrate>> user:{} data:{}".format(self.current_user.todict(), args))
        start_date, end_date, price = get_and_valid_arguments(args,
                'start_date', 'end_date', 'price')
        weekdays = args.get('weekdays', None)

        self.valid_price(price)
        start_date, end_date = self.valid_date(start_date, end_date, weekdays)

        roomrate = self.set_price(roomrate_id, price, start_date, end_date, weekdays)
        if roomrate:
            self.finish_json(result=dict(
                roomrate=roomrate.todict(),
                ))
        else:
            raise JsonException(errmsg="修改失败", errcode=1001)



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

    def set_price(self, roomrate_id, price, start_date, end_date, weekdays=None):
        roomrate = RoomRateModel.set_price(self.db, roomrate_id, price, start_date, end_date, weekdays)
        if roomrate:
            PushRatePlanTask().push_rateplan.delay(roomrate.rate_plan_id, with_cancel_rule=False)
        return roomrate


