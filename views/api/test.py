# -*- coding: utf-8 -*-
import re

from tornado.escape import json_encode
from tornado import gen, web


from views import BaseHandler
from views.base import BtwBaseHandler
from tools.auth import auth_login
from tools.auth import auth_permission
from constants import PERMISSIONS
from tools.request_tools import get_and_valid_arguments
from models.order_history import OrderHistoryModel

from tasks import test as Test
from tools.request_tools import clear_domain_cookie

class HelloWorldHandler(BtwBaseHandler):

    def get(self):
        self.clear_cookie("open_id", domain=".betterwood.com")
        clear_domain_cookie(self, "username", domain=".betterwood.com")
        self.clear_cookie("merchant_id", domain=".betterwood.com")
        self.clear_all_cookies()
        self.finish('hello world')

class HelloWorldCeleryHandler(BtwBaseHandler):

    @gen.coroutine
    def get(self):
        self.set_secure_cookie("username", self.current_user.username, domain=".betterwood.com")

class LockTestHandler(BtwBaseHandler):

    @web.asynchronous
    def get(self):
        r = OrderHistoryModel.get_lock_test(self.db, 21)
        print r
