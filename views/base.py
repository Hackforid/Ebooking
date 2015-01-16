# -*- coding: utf-8 -*-

import sys
import traceback

from tornado.escape import json_decode
from tornado.util import ObjectDict
from tornado import gen

from views import BaseHandler
from exception.json_exception import JsonException, JsonDecodeError

from tools.json import json_encode

from tasks.models import user as User
from mixin.request_mixin import CeleryTaskMixin

import tcelery
tcelery.setup_nonblocking_producer()


class BtwBaseHandler(BaseHandler, CeleryTaskMixin):

    def initialize(self):
        super(BtwBaseHandler, self).initialize()
        self.current_user = None
        self.merchant = None

    @gen.coroutine
    def prepare(self):
        yield self.get_current_user()

    @gen.coroutine
    def get_current_user(self):
        username = self.get_secure_cookie('username')
        merchant_id = self.get_secure_cookie('merchant_id')
        if username and merchant_id:
            self.set_secure_cookie('username', username, expires_days=0.02)
            self.set_secure_cookie('merchant_id', merchant_id, expires_days=0.02)
            task = yield gen.Task(User.get_login_user.apply_async,
                args=[merchant_id, username])
            if task.status == 'SUCCESS':
                self.merchant, self.current_user = task.result
        raise gen.Return(self.current_user)

    def render(self, template_name, **kwargs):
        kwargs['current_user'] = self.current_user
        if self.current_user:
            super(BtwBaseHandler, self).render(template_name, merchant=self.merchant, user=self.current_user, **kwargs) 
        else:
            super(BtwBaseHandler, self).render(template_name, **kwargs) 

    def _handle_request_exception(self, e):
        if isinstance(e, JsonException):
            print e.tojson()
            self.finish_json(errcode=e.errcode, errmsg=e.errmsg)
        else:
            super(BtwBaseHandler, self)._handle_request_exception(e)

    def finish_json(self, errcode=0, errmsg=None, result=None):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        self.finish(json_encode({'errcode': errcode,
                    'errmsg': errmsg,
                                 'result': result}))

    def get_json_arguments(self, raise_error=True):
        try:
            return ObjectDict(json_decode(self.request.body))
        except Exception, e:
            print traceback.format_exc()
            if raise_error:
                raise JsonDecodeError()

