# -*- coding: utf-8 -*-

from tornado.escape import json_encode, json_decode
from tornado.util import ObjectDict

from views.base import BtwBaseHandler
from models.user import UserModel

from tools.auth import auth_login, auth_permission


class Login

