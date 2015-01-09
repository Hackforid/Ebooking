# -*- coding: utf-8 -*-

from views.base import BtwBaseHandler

from tools.auth import auth_login, auth_permission
from constants import PERMISSIONS

class OrderWaitingHandler(BtwBaseHandler):

    @auth_login()
    @auth_permission(PERMISSIONS.admin | PERMISSIONS.update_order)
    def get(self):
        self.render("orderWaiting.html")
