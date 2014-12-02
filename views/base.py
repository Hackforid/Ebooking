# -*- coding: utf-8 -*-

import sys
import traceback

from tornado.escape import json_encode, json_decode
from tornado.util import ObjectDict

from views import BaseHandler
from models.user import UserModel
from exception.json_exception import JsonException, JsonDecodeError


class BtwBaseHandler(BaseHandler):

    def initialize(self):
        super(BtwBaseHandler, self).initialize()
        self.current_user = None

    def prepare(self):
        self.get_current_user()

    def get_current_user(self):
        username = self.get_secure_cookie('username')
        merchant_id = self.get_secure_cookie('merchant_id')
        if username and merchant_id:
            self.set_secure_cookie('username', username, expires_days=0.02)
            self.set_secure_cookie('merchant_id', merchant_id, expires_days=0.02)
        self.current_user = UserModel.get_user_by_merchantid_username(self.db, merchant_id, username)
        return self.current_user

    def render(self, template_name, **kwargs):
        kwargs['current_user'] = self.current_user
        super(BtwBaseHandler, self).render(template_name, **kwargs)

    def _handle_request_exception(self, e):
        self.db.rollback()
        if isinstance(e, JsonException):
            self.log_exception(*sys.exc_info())
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

