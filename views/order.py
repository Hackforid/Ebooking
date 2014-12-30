# -*- coding: utf-8 -*-

from views.base import BtwBaseHandler

from tools.auth import auth_login

class OrderWaitingHandler(BtwBaseHandler):

    @auth_login()
    def get(self):
        self.render("orderWaiting.html")
