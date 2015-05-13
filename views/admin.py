# -*- coding: utf-8 -*-

from tornado import gen
from tools.auth import auth_backstage_login

from views.base import BackStageHandler


class AdminHandler(BackStageHandler):

    @auth_backstage_login()
    def get(self):
        self.render("admin.html")

class MerchantHotelsHandler(BackStageHandler):

    @auth_backstage_login()
    def get(self, merchant_id):
        self.render("adminHotels.html", merchant_id=merchant_id)

