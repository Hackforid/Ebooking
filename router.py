# -*- coding: utf8 -*-

from views.api.test import HelloWorldHandler, HelloWorldCeleryHandler
from views.login import LoginHandler, LogoutHandler
from views.user import UserManageHandler
from views.hotel_will_coop import HotelWillCoopHandler
from views.hotel_cooped import HotelCoopedHandler
from views.hotel_inventory import HotelInventoryHandler
from views.rateplan import RatePlanHandler
from views.order import OrderWaitingHandler
from views.order_list import OrderListHandler
from views.api.city import CityAPIHandler, DistrictByCityAPIHandler
from views.api.hotel_will_coop import HotelWillCoopAPIHandler
from views.api.hotel_coop import HotelCoopAPIHandler, HotelCoopsAPIHandler 
from views.api.hotel_cooped import HotelCoopedAPIHandler, HotelCoopOnlineAPIHandler, HotelCoopedModifyAPIHandler
from views.api.user import UserManageAPIHandler
from views.password import PasswordHandler
from views.api.password import PasswordAPIHandler
from views.api.hotel import HotelAPIHandler
from views.api.roomtype_cooped import RoomTypeCoopedAPIHandler, RoomTypeCoopedModifyAPIHandler, RoomTypeOnlineAPIHandler, RoomTypeByMerchantOnlineAPIHandler
from views.api.rateplan import RatePlanAPIHandler, RatePlanModifyAPIHandler
from views.api.submit_order import SubmitOrderAPIHandler, CancelOrderAPIHander
from views.api.roomrate import RoomRateAPIHandler
from views.api.inventory import InventoryAPIHandler, InventoryCompleteAPIHandler
from views.api.order import OrderWaitingAPIHandler, OrderTodayBookListAPIHandler, OrderTodayCheckinListAPIHandler, OrderUserConfirmAPIHandler, OrderUserCancelAPIHandler, OrderSearchAPIHandler

from views.api.merchant import MerchantListAPIHandler, MerchantQueryByHotelAPIHandler

from views.api.console import POIPushAllAPIHandler, StockPushAllAPIHandler
from views.api.finance import FinanceAPIHandler, IncomeAPIHandler
from views.finance import FinanceAgencyHandler, FinancePrepayHandler
from views.api.contract import ContractAPIHandler
from views.contract import ContractHandler

from views.api.pms import PMSNewOrderAPIHandler
from views.api.batch import HotelRoomBatchAPIHandler

handlers = [
        (r"/?", OrderWaitingHandler),
        (r"/login/?", LoginHandler),
        (r"/logout/?", LogoutHandler),
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
        (r"/api/hotel/coops/?", HotelCoopsAPIHandler),
        (r"/api/hotel/cooped/?", HotelCoopedAPIHandler),
        (r"/api/hotel/cooped/(?P<hotel_id>\d+)/?", HotelCoopedModifyAPIHandler),
        (r"/api/hotel/(?P<hotel_id>\d+)/roomtype/(?P<roomtype_id>\d+)/cooped/?", RoomTypeCoopedModifyAPIHandler),
        (r"/api/hotel/(?P<hotel_id>\d+)/roomtype/(?P<roomtype_id>\d+)/online/?", RoomTypeOnlineAPIHandler),
        (r"/api/merchant/roomtype/online/?", RoomTypeByMerchantOnlineAPIHandler),
        (r"/api/hotel/cooped/(?P<hotel_id>\d+)/online/(?P<is_online>\d+)/?", HotelCoopOnlineAPIHandler),

        (r"/api/hotel/(?P<hotel_id>\d+)/roomtype/?", RoomTypeCoopedAPIHandler),

        (r"/hotel/cooped/(?P<hotel_id>\d+)/rateplan/?", RatePlanHandler),
        (r"/api/hotel/(?P<hotel_id>\d+)/roomtype/(?P<roomtype_id>\d+)/rateplan/?", RatePlanAPIHandler),
        (r"/api/hotel/(?P<hotel_id>\d+)/roomtype/(?P<roomtype_id>\d+)/rateplan/(?P<rateplan_id>\d+)/?", RatePlanModifyAPIHandler),
        (r"/api/hotel/(?P<hotel_id>\d+)/roomtype/(?P<roomtype_id>\d+)/roomrate/(?P<roomrate_id>\d+)/?", RoomRateAPIHandler),

        (r"/api/hotel/(?P<hotel_id>\d+)/roomtype/(?P<roomtype_id>\d+)/inventory/?", InventoryAPIHandler),



        (r"/order/waiting/?", OrderWaitingHandler),
        (r"/api/order/waiting/?", OrderWaitingAPIHandler),
        (r"/api/order/(?P<order_id>\d+)/confirm/?", OrderUserConfirmAPIHandler),
        (r"/api/order/(?P<order_id>\d+)/cancel/?", OrderUserCancelAPIHandler),

        (r"/order/list/?", OrderListHandler),
        (r"/api/order/todaybook/?", OrderTodayBookListAPIHandler),
        (r"/api/order/todaycheckin/?", OrderTodayCheckinListAPIHandler),
        (r"/api/order/search/?", OrderSearchAPIHandler),
        (r"/api/inventory/complete/?", InventoryCompleteAPIHandler),

        (r"/api/test/helloworld", HelloWorldHandler),
        (r"/api/test/helloworld/celery/?", HelloWorldCeleryHandler),

        (r"/admin/?", "views.admin.AdminHandler"),
        (r"/admin/merchant/(?P<merchant_id>\d+)/hotels/?", "views.admin.MerchantHotelsHandler"),
        (r"/admin/merchant/(?P<merchant_id>\d+)/hotel/(?P<hotel_id>\d+)/contract/?", "views.admin.HotelContractHandler"),

        (r"/api/admin/merchant/all/?", "views.api.admin.merchant.AdminMerchantAPIHandler"),
        (r"/api/admin/merchant/modify/?", "views.api.admin.merchant.AdminMerchantModifyAPIHandler"),
        (r"/api/admin/merchant/(?P<merchant_id>\d+)/suspend/(?P<is_suspend>\d+)/?", "views.api.admin.merchant.AdminMerchantSuspendAPIHandler"),
        (r"/api/admin/merchant/(?P<merchant_id>\d+)/hotels/?", "views.api.admin.merchant.MerchantHotelsAPIHandler"),
        (r"/api/admin/merchant/(?P<merchant_id>\d+)/hotel/(?P<hotel_id>\d+)/contract/?", "views.api.admin.contract.HotelContractAPIHandler"),
        (r"/api/admin/merchant/(?P<merchant_id>\d+)/hotel/(?P<hotel_id>\d+)/roomtype/(?P<roomtype_id>\d+)/pay_type/(?P<pay_type>\d+)/contract/?", "views.api.admin.contract.RoomTypeContractAPIHandler"),


        (r"/api/merchant/all/?", MerchantListAPIHandler),

        (r"/api/poi/push/all/?", POIPushAllAPIHandler),
        (r"/api/stock/push/all/?", StockPushAllAPIHandler),
        (r"/api/finance/?", FinanceAPIHandler),
        (r"/api/income/?", IncomeAPIHandler),
        (r"/finance/prepay/?", FinancePrepayHandler),
        (r"/finance/agency/?", FinanceAgencyHandler),


        (r"/api/contract/?", ContractAPIHandler),
        (r"/contract/?", ContractHandler),

        (r"/api/inner/ordersys/order/submit/?", SubmitOrderAPIHandler),
        (r"/api/inner/ordersys/order/(?P<order_id>\d+)/cancel/?", CancelOrderAPIHander),
        (r"/api/pms/merchant/(?P<merchant_id>\d+)/order/new/?", PMSNewOrderAPIHandler),

        (r"/api/batch/online/?", HotelRoomBatchAPIHandler),
        (r"/api/inner/merchant/query/hotel/(?P<hotel_id>\d+)/?", MerchantQueryByHotelAPIHandler),

        (r"/api/city/(?P<city_id>\d+)/district/?", DistrictByCityAPIHandler),
        
]
