# -*- coding: utf-8 -*-
import re

from tornado.escape import json_encode
from tornado import gen


from views import BaseHandler
from views.base import BtwBaseHandler
from tools.auth import auth_login
from tools.auth import auth_permission
from constants import PERMISSIONS
from tools.request_tools import get_and_valid_arguments

from tasks import test as Test

class HelloWorldHandler(BtwBaseHandler):

    def get(self):
        self.finish('hello world')

class HelloWorldCeleryHandler(BaseHandler):

    @gen.coroutine
    def get(self):
        task = yield gen.Task(Test.helloworld.apply_async)
        self.finish(task.result)
