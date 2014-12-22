# -*- coding: utf-8 -*-

from views.base import BtwBaseHandler

from tools.auth import auth_login

class OrderWaitingHandler(BtwBaseHandler):

    def get(self):
        self.render("orderWaiting.html")
