# -*- coding: utf-8 -*-

from datetime import datetime, timedelta, date

from tornado import gen
from tornado.httpclient import AsyncHTTPClient
from tornado.escape import json_encode, json_decode, url_escape

from config import API
from constants import PERMISSIONS
from tools.auth import auth_login, auth_permission
from tools.url import add_get_params
from tools.request_tools import get_and_valid_arguments
from views.base import BtwBaseHandler
from exception.json_exception import JsonException

import tasks.models.inventory as Inventory
import tcelery
tcelery.setup_nonblocking_producer()

from tools.log import Log

class InventoryAPIHandler(BtwBaseHandler):

    @gen.coroutine
    @auth_login(json=True)
    @auth_permission(PERMISSIONS.admin | PERMISSIONS.inventory, json=True)
    def put(self, hotel_id, roomtype_id):
        merchant_id = self.current_user.merchant_id
        args = self.get_json_arguments()
        Log.info(u"modify inventory>> user:{} data:{}".format(self.current_user.todict(), args))
        start_date, end_date, change_num, price_type = get_and_valid_arguments(args,
                'start_date', 'end_date', 'change_num', 'price_type')
        start_date, end_date = self.valid_date(start_date, end_date)
        self.valid_args(price_type)

        change_task = yield gen.Task(Inventory.modify_inventory.apply_async,
                args=[merchant_id, hotel_id, roomtype_id, price_type, change_num, start_date, end_date])
        inventories = change_task.result
        if inventories:
            print 'success'
            self.finish_json(result=dict(
                inventories = [inventory.todict() for inventory in inventories],
                ))
        else:
            raise JsonException(errcode=2002, errmsg="change fail")


    def valid_args(self, price_type):
        if price_type not in [0, 1]:
            raise JsonException(errcode=2001, errmsg="invalid price type")



    def valid_date(self, str_start_date, str_end_date):
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

        if start_date.date() < min_date or start_date.date() > max_date:
            raise JsonException(errcode=2001, errmsg="invalid date: start date out of range")

        if end_date.date() < min_date or end_date.date() > max_date:
            raise JsonException(errcode=2001, errmsg="invalid date: end date out of range")

        return start_date, end_date

class InventoryCompleteAPIHandler(BtwBaseHandler):

    @gen.coroutine
    @auth_login(json=True)
    @auth_permission(PERMISSIONS.admin | PERMISSIONS.inventory, json=True)
    def get(self):
        yield gen.Task(Inventory.complete_in_four_months.apply_async,
                args=[])
        self.finish_json()

