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

from tasks.poi import POIPushTask
from tasks.models.merchant import get_merchant_list
from tasks.stock import PushHotelTask


class POIPushAllAPIHandler(BtwBaseHandler):

    @auth_login(json=True)
    @auth_permission(PERMISSIONS.admin, json=True)
    def get(self):
        POIPushTask().push_all.delay()
        self.finish_json(errcode=0, result=[])


class StockPushAllAPIHandler(BtwBaseHandler):

    @auth_login(json=True)
    @auth_permission(PERMISSIONS.admin, json=True)
    def get(self):
        PushHotelTask().push_all.delay()
        self.finish_json(errcode=0, result=[])
