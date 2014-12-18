# -*- coding: utf-8 -*-

from datetime import datetime, timedelta

from tornado import gen
from tornado.escape import json_encode, json_decode, url_escape

from tools.auth import auth_login
from tools.request_tools import get_and_valid_arguments
from views.base import BtwBaseHandler
from exception.json_exception import JsonException

import tasks.models.room_rate as  RoomRate


import tcelery
tcelery.setup_nonblocking_producer()

class RoomRateAPIHandler(BtwBaseHandler):

    @gen.coroutine
    @auth_login(json=True)
    def put(self, hotel_id, roomtype_id, roomrate_id):
        args = self.get_json_arguments()
        start_date, end_date, price = get_and_valid_arguments(args,
                'start_date', 'end_date', 'price')

        self.valid_price(price)
        start_date, end_date = self.valid_date(start_date, end_date)

        roomrate = yield self.set_price(roomrate_id, price, start_date, end_date)
        if roomrate:
            self.finish_json(result=dict(
                roomrate=roomrate.todict(),
                ))
        else:
            raise JsonException(errmsg="修改失败", errcode=1001)



    def valid_date(self, str_start_date, str_end_date):
        time_format = "%Y-%m-%d"
        try:
            start_date = datetime.strptime(str_start_date, time_format)
            end_date = datetime.strptime(str_end_date, time_format)
        except:
            raise JsonException(errcode=2001, errmsg="invalid date")

        if end_date < start_date:
            raise JsonException(errcode=2001, errmsg="invalid date")

        min_date = datetime.today()
        max_date = min_date + timedelta(days=90)

        if start_date < min_date or start_date > max_date:
            raise JsonException(errcode=2001, errmsg="invalid date")

        if end_date < min_date or end_date > max_date:
            raise JsonException(errcode=2001, errmsg="invalid date")

        return start_date, end_date

    def valid_price(self, price):
        # range [0, 2^31]
        if not isinstance(price, int) or price < 0 or price > 2147483647:
            raise JsonException(errcode=2002, errmsg="invalid price")

    @gen.coroutine
    def set_price(self, roomrate_id, price, start_date, end_date):
        task = yield gen.Task(RoomRate.set_price.apply_async,
                args=[roomrate_id, price, start_date, end_date])

        raise gen.Return(task.result)


