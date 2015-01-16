# -*- coding: utf-8 -*-

from views.base import BtwBaseHandler

from tools.auth import auth_login, auth_permission, no_monomer_hotel
from tools.request_tools import get_and_valid_arguments
from constants import PERMISSIONS

class HotelWillCoopHandler(BtwBaseHandler):

    @auth_login()
    @no_monomer_hotel()
    def get(self):
        self.render("hotelWillCoop.html")
