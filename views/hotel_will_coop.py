# -*- coding: utf-8 -*-

from views.base import BtwBaseHandler

from tools.auth import auth_login
from tools.request_tools import get_and_valid_arguments

class HotelWillCoopHandler(BtwBaseHandler):

    def get(self):
        self.render("hotelWillCoop.html")