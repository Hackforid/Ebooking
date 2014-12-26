# -*- coding: utf-8 -*-

from views.base import BtwBaseHandler

from tools.auth import auth_login
from tools.request_tools import get_and_valid_arguments

class HotelCoopedHandler(BtwBaseHandler):

    @auth_login()
    def get(self):
        self.render("hotelCoop.html")
