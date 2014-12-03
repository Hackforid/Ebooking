# -*- coding: utf8 -*-

from views.login import LoginHandler
from views.hotel_will_coop import HotelWillCoopHandler
from views.hotel_cooped import HotelCoopedHandler
from views.api.city import CityAPIHandler
from views.api.hotel_will_coop import HotelWillCoopAPIHandler
from views.api.hotel_coop import HotelCoopAPIHandler
from views.api.hotel_cooped import HotelCoopedAPIHandler


handlers = [
        (r"/login/?", LoginHandler),
        (r"/hotel/willcoop/?", HotelWillCoopHandler),
        (r"/hotel/cooped/?", HotelCoopedHandler),
        (r"/api/city/?", CityAPIHandler,),
        (r"/api/hotel/willcoop/?", HotelWillCoopAPIHandler),
        (r"/api/hotel/coop/(?P<hotel_id>\d+)/?", HotelCoopAPIHandler),
        (r"/api/hotel/cooped/?", HotelCoopedAPIHandler),
        ]
