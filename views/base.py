# -*- coding: utf-8 -*-

import sys
import traceback
import json

from tornado.escape import json_decode
from tornado.util import ObjectDict
from tornado import gen
from tornado.httpclient import AsyncHTTPClient

from views import BaseHandler
from exception.json_exception import JsonException, JsonDecodeError

from tools.json import json_encode

from mixin.request_mixin import CeleryTaskMixin
from models.user import UserModel
from models.merchant import MerchantModel
from tools.log import Log

from config import BACKSTAGE_HOST, BACKSTAGE_USERNAME_KEY

import tcelery
tcelery.setup_nonblocking_producer()


class BtwBaseHandler(BaseHandler, CeleryTaskMixin):

    def initialize(self):
        super(BtwBaseHandler, self).initialize()
        self.db = self.application.DB_Session()
        self.current_user = None
        self.merchant = None
        self.is_jsonp = False
        self.callback_fun_name = ""

    def prepare(self):
        self.get_current_user()
        if self.get_argument('jsonp', None):
            self.is_jsonp = True
            self.request.method = self.get_argument('method', 'GET')
            body = self.get_argument('body', None)
            self.callback_fun_name = self.get_argument('callback')
            if self.request.method in ['POST', 'PUT']:
                if body is not None:
                    self.request.body = body

    def on_finish(self):
        self.db.close()

    def get_current_user(self):
        username = self.get_secure_cookie('username')
        merchant_id = self.get_secure_cookie('merchant_id')
        if username and merchant_id:
            self.set_secure_cookie('username', username, expires_days=0.02)
            self.set_secure_cookie('merchant_id', merchant_id, expires_days=0.02)
            self.merchant = MerchantModel.get_by_id(self.db, merchant_id)
            self.current_user = UserModel.get_user_by_merchantid_username(self.db, merchant_id, username)
        return self.current_user

    def render(self, template_name, **kwargs):
        kwargs['current_user'] = self.current_user
        if self.current_user:
            super(BtwBaseHandler, self).render(template_name, merchant=self.merchant, user=self.current_user, **kwargs) 
        else:
            super(BtwBaseHandler, self).render(template_name, **kwargs) 

    def _handle_request_exception(self, e):
        self.db.rollback()
        if isinstance(e, JsonException):
            print e.tojson()
            self.finish_json(errcode=e.errcode, errmsg=e.errmsg)
        else:
            super(BtwBaseHandler, self)._handle_request_exception(e)

    def finish_json(self, errcode=0, errmsg=None, result=None):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        #self.set_header("Access-Control-Allow-Origin", "*")
        resp_json = json_encode({'errcode': errcode,
                    'errmsg': errmsg,
                                 'result': result})
        if self.is_jsonp:
            resp_json = "{}({})".format(self.callback_fun_name, resp_json)
        self.finish(resp_json)

    def get_json_arguments(self, raise_error=True):
        try:
            return ObjectDict(json_decode(self.request.body))
        except Exception, e:
            print traceback.format_exc()
            if raise_error:
                raise JsonDecodeError()

class BackStageHandler(BtwBaseHandler):

    def initialize(self):
        super(BackStageHandler, self).initialize()
        self.backstage_user_name = None
        self.backstage_user_permissions = []

    @gen.coroutine
    def prepare(self):
        yield self.get_backstage_user()

    @gen.coroutine
    def get_backstage_user(self):
        self.backstage_user_name = self.get_secure_cookie(BACKSTAGE_USERNAME_KEY)
        if self.backstage_user_name:
            yield self.get_backstage_user_permission(self.backstage_user_name)

        raise gen.Return()

    @gen.coroutine
    def get_backstage_user_permission(self, username):
        url = '{}/app/supplier_manage/list?username={}'.format(BACKSTAGE_HOST, username)
        resp = yield AsyncHTTPClient().fetch(url)
        r = json.loads(resp.body)
        resources = r['result']['resources']
        self.backstage_user_permissions = [p['id'] for p in resources]
        raise gen.Return()



