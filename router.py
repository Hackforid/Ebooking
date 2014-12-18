# -*- coding: utf8 -*-

from views.login import LoginHandler
from views.user import UserManageHandler
from views.hotel_will_coop import HotelWillCoopHandler
from views.hotel_cooped import HotelCoopedHandler
from views.hotel_inventory import HotelInventoryHandler
from views.rateplan import RatePlanHandler
from views.api.city import CityAPIHandler
from views.api.hotel_will_coop import HotelWillCoopAPIHandler
from views.api.hotel_coop import HotelCoopAPIHandler
from views.api.hotel_cooped import HotelCoopedAPIHandler
from views.api.user import UserManageAPIHandler
from views.password import PasswordHandler
from views.api.password import PasswordAPIHandler
from views.api.hotel import HotelAPIHandler
from views.api.roomtype_cooped import RoomTypeCoopedAPIHandler
from views.api.rateplan import RatePlanAPIHandler, RatePlanModifyAPIHandler
#from views.api.submit_order import SubmitOrderAPIHandler
from views.api.roomrate import RoomRateAPIHandler

handlers = [
        (r"/login/?", LoginHandler),
        (r"/hotel/willcoop/?", HotelWillCoopHandler),
        (r"/hotel/cooped/?", HotelCoopedHandler),
        (r"/userManage/?", UserManageHandler),
        (r"/api/userManage/?", UserManageAPIHandler),
        (r"/password/?", PasswordHandler),
        (r"/api/password/?", PasswordAPIHandler),

        (r"/hotel/cooped/(?P<hotel_id>\d+)/inventory/?", HotelInventoryHandler),

        (r"/api/hotel/(?P<hotel_id>\d+)/?", HotelAPIHandler),
        (r"/api/city/?", CityAPIHandler,),
        (r"/api/hotel/willcoop/?", HotelWillCoopAPIHandler),
        (r"/api/hotel/coop/(?P<hotel_id>\d+)/?", HotelCoopAPIHandler),
        (r"/api/hotel/cooped/?", HotelCoopedAPIHandler),

        (r"/api/hotel/(?P<hotel_id>\d+)/roomtype/?", RoomTypeCoopedAPIHandler),

        (r"/hotel/cooped/(?P<hotel_id>\d+)/rateplan/?", RatePlanHandler),
        (r"/api/hotel/(?P<hotel_id>\d+)/roomtype/(?P<roomtype_id>\d+)/rateplan/?", RatePlanAPIHandler),
        (r"/api/hotel/(?P<hotel_id>\d+)/roomtype/(?P<roomtype_id>\d+)/rateplan/(?P<rateplan_id>\d+)/?", RatePlanModifyAPIHandler),
        (r"/api/hotel/(?P<hotel_id>\d+)/roomtype/(?P<roomtype_id>\d+)/roomrate/(?P<roomrate_id>\d+)/?", RoomRateAPIHandler),

#        (r"/api/hotel/submitorder/?", SubmitOrderAPIHandler),
]
