# -*- coding: utf-8 -*-

from views.base import BtwBaseHandler
from tools.auth import auth_login

class ContractHandler(BtwBaseHandler):

    @auth_login()
    def get(self):
        self.render("contract.html")

