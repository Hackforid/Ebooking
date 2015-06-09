# -*- coding: utf-8 -*-

import json

from tornado import gen
from tornado.httpclient import AsyncHTTPClient

from config import API
from exception.json_exception import JsonException
from tools.log import Log


from tools.request_tools import clear_domain_cookie

class WechatMixin(object):

    @gen.coroutine
    def valid_wechat_login(self):
        open_id = self.get_secure_cookie("open_id", None)
        if not open_id:
            raise gen.Return(True)

        username = self.get_secure_cookie('username')
        merchant_id = self.get_secure_cookie('merchant_id')
        r = yield self.check_open_id(open_id, merchant_id, username)
        raise gen.Return(r)

    @gen.coroutine
    def check_open_id(self, open_id, merchant_id, username):
        if API.get('WEIXIN') is None:
            raise gen.Return(False)
        url = "{}/webchart/user/ebk/has_bind_wechat?merchantId={}&username={}&openId={}".format(API['WEIXIN'], merchant_id, username, open_id)
        resp = yield AsyncHTTPClient().fetch(url)
        Log.info(resp.body)
        if resp.code == 200:
            r = json.loads(resp.body)
            if r and r['errcode'] == 0:
                raise gen.Return(True)
            else:
                self.logout()
                raise gen.Return(False)
        else:
            raise JsonException(500, 'call weixin server error')

    def logout(self):
        Log.info("valid weixin fail")
        clear_domain_cookie(self, "open_id", domain=".betterwood.com")
        clear_domain_cookie(self, "username", domain=".betterwood.com")
        clear_domain_cookie(self, "merchant_id", domain=".betterwood.com")
        clear_domain_cookie(self, "open_id")
        clear_domain_cookie(self, "username")
        clear_domain_cookie(self, "merchant_id")
        raise JsonException(500, "weixin login valid fai")



