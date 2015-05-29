# -*- coding: utf-8 -*-


import time
import urllib
import json
from tornado.escape import json_encode, json_decode, url_escape
from tornado import gen
from tornado.httpclient import AsyncHTTPClient

from views.base import BtwBaseHandler
from exception.json_exception import JsonException

from config import API

class QRCodeAPIHandler(BtwBaseHandler):

    @gen.coroutine
    def get(self):
        url = "{}/webchart/user/ebk/get_2dcode?merchantId={}&merchantName={}&username={}".format(API['WEIXIN'], self.merchant.id, self.merchant.name, self.current_user.username)
        print url
        resp = yield AsyncHTTPClient().fetch(url)
        r = json_decode(resp.body)
        if r and r['errcode'] == 0:
            self.finish_json(result=dict(
                url=r['result']['url']
                ))
        else:
            raise JsonException(1000, 'error')

