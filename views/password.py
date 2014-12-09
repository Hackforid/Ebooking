# -*- coding: utf-8 -*-
from views.base import BtwBaseHandler
from tools.auth import auth_login
from tools.auth import auth_permission
from constants import PERMISSIONS

class PasswordHandler(BtwBaseHandler):

    @auth_login()
    @auth_permission(PERMISSIONS.update_password)
    def get(self):
        return self.render('password.html')
