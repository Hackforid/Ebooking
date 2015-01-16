# -*- coding: utf-8 -*-

from tornado import gen

from views.base import BtwBaseHandler


class AdminHandler(BtwBaseHandler):

    def get(self):
        self.render("admin.html")
