# -*- coding: utf-8 -*-

from views.base import BtwBaseHandler
from models.user import UserModel

from tools.auth import auth_login

class LoginHandler(BtwBaseHandler):

    def get(self):
        self.render("index.html")
