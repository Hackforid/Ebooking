# -*- coding: utf-8 -*-

from tornado import gen
from tornado.httpclient import AsyncHTTPClient
from tornado.escape import json_encode, json_decode

from config import API
from views.base import BtwBaseHandler

class CityAPIHandler(BtwBaseHandler):

    @gen.coroutine
    def get(self):
        citys = yield self.fetch_city()
        self.finish_json(result={
            'citys': citys,
        })

    @gen.coroutine
    def fetch_city(self):
        url = API['POI'] + '/api/city/'
        resp = yield AsyncHTTPClient().fetch(url)

        r = json_decode(resp.body)

        if r and r['errcode'] == 0:
            citys = r['result']['citys']
            raise gen.Return(citys)
        else:
            raise gen.Return([])