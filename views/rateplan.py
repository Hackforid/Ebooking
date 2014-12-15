# -*- coding: utf-8 -*-

from views.base import BtwBaseHandler

from tools.auth import auth_login
from tools.request_tools import get_and_valid_arguments

class RatePlanHandler(BtwBaseHandler):

    def get(self, hotel_id):
        self.render("ratePlan.html", hotel_id=hotel_id)

