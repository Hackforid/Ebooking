# -*- coding: utf-8 -*-

from tornado import gen
from tools.auth import need_btw_admin, auth_login

from views.base import BtwBaseHandler


class AdminHandler(BtwBaseHandler):

    @auth_login()
    @need_btw_admin()
    def get(self):
        self.render("admin.html")
