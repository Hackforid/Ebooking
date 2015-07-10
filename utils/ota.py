# -*- coding: utf-8 -*-

import time
import urllib
import json

from tornado.escape import json_encode, json_decode, url_escape
from tornado import gen
from tornado.httpclient import AsyncHTTPClient
from tornado.escape import json_encode, json_decode, url_escape

from exception.json_exception import JsonException
from tools.log import Log
from config import API, IS_PUSH_TO_STOCK

CHAIN_ID = 6

def generate_track_id(data):
    return "{}|{}".format(data, time.time())

@gen.coroutine
def get_all_ota():
    url = '{}/hotelReader2/ota/getList'.format(API['OTA'])
    try:
        r = yield AsyncHTTPClient().fetch(url)
        resp = json_decode(r.body)
    except Exception, e:
        raise gen.Return([])
    if resp['errcode'] == 0:
        raise gen.Return(resp['result'])
    else:
        raise gen.Return([])

@gen.coroutine
def change_ota(hotel_id, ota_ids):
    Log.info("change ota>>hotel {}>>ota {}".format(hotel_id, ota_ids))
    url =  API['STOCK'] + '/stock/switch_ota'
    track_id = generate_track_id(hotel_id)
    if not ota_ids:
        ota_ids_str = '-1'
    else:
        ota_ids_str = '|'.join([str(id) for id in ota_ids])
    data = {
            'track_id': track_id,
            'chain_id': CHAIN_ID,
            'chain_hotel_id': hotel_id,
            'ota_ids': ota_ids_str,
            }
    body = urllib.urlencode(data)
    Log.info("change ota>>hotel {}>>ota {}:req {}".format(hotel_id, ota_ids, body))

    if not IS_PUSH_TO_STOCK:
        raise gen.Return(True)

    try:
        r = yield AsyncHTTPClient().fetch(url, method='POST', body=body)
        Log.info("change ota>>hotel {}>>ota {}:resp {}".format(hotel_id, ota_ids, r.body))
        resp = json.loads(r.body)
    except Exception, e:
        Log.exception(e)
        raise gen.Return(False)
    if resp['errcode'] == 0:
        raise gen.Return(True)
    else:
        raise gen.Return(False)

