# -*- coding: utf-8 -*-

from views.base import BtwBaseHandler
from tools.auth import auth_login

class FinancePrepayHandler(BtwBaseHandler):

    @auth_login()
    def get(self):
        self.render("financePrepay.html")

class FinanceAgencyHandler(BtwBaseHandler):

    @auth_login()
    def get(self):
        self.render("financeAgency.html")
