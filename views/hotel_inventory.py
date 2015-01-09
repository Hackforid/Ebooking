# -*- coding: utf-8 -*-

from views.base import BtwBaseHandler

from tools.auth import auth_login, auth_permission
from tools.request_tools import get_and_valid_arguments
from constants import PERMISSIONS

class HotelInventoryHandler(BtwBaseHandler):

    @auth_login()
    def get(self, hotel_id):
        self.render("hotelInventory.html", hotel_id=hotel_id)
