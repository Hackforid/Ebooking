# -*- coding: utf-8 -*-
from views.base import BtwBaseHandler
from tools.auth import auth_login, auth_permission
from constants import PERMISSIONS

class PasswordHandler(BtwBaseHandler):

    @auth_login()
    def get(self):
        return self.render('password.html')
