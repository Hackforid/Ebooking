# -*- coding: utf-8 -*-

from views.base import BtwBaseHandler
from tools.auth import auth_login

class FinanceHandler(BtwBaseHandler):

    @auth_login()
    def get(self):
        self.render("finance.html")
