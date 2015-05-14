# -*- coding: utf-8 -*-

import json

from tornado import gen
from tornado.httpclient import AsyncHTTPClient
from tornado.escape import url_escape

from config import API

@gen.coroutine
def get_base_hotel_info(hotel_id):
    url = "{}/api/hotel/{}".format(API['POI'], hotel_id)
    resp = yield AsyncHTTPClient().fetch(url)
    r = json.loads(resp.body)
    if r and r['errcode'] == 0:
        hotel = r['result']['hotel']
    else:
        hotel = None

    raise gen.Return(hotel)


@gen.coroutine
def get_base_hotel_and_roomtypes_info(hotel_id):
    url = "{}/api/hotel/{}/roomtype".format(API['POI'], hotel_id)
    resp = yield AsyncHTTPClient().fetch(url)
    r = json.loads(resp.body)
    if r and r['errcode'] == 0:
        hotel = r['result']['hotel']
        roomtypes = r['result']['roomtypes']
    else:
        hotel = None
        roomtypes = None

    raise gen.Return((hotel, roomtypes))

