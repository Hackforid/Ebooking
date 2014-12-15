# -*- coding: utf-8 -*-

from tornado import gen
from tornado.httpclient import AsyncHTTPClient
from tornado.escape import json_encode, json_decode, url_escape

from config import API
from tools.auth import auth_login
from tools.url import add_get_params
from views.base import BtwBaseHandler
from exception.json_exception import JsonException


class HotelAPIHandler(BtwBaseHandler):

    @gen.coroutine
    def get(self, hotel_id):
        resp = yield AsyncHTTPClient().fetch(API['POI'] + "/api/hotel/" + hotel_id)
        r = json_decode(resp.body)

        if r and r['errcode'] == 0:
            self.finish_json(result=dict(
                hotel=r['result']['hotel']
                ))
        else:
            raise JsonException(errcode=404, errmsg="hotel not found")

