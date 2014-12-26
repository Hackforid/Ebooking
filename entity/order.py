# -*- coding: utf-8 -*-

import json

class SubmitOrder(object):

    def __init__(self, req_json):
       o = json.loads(req_json)
       self.id = o.get('id', 0)
       self.city_id = o.get('cityId', 0)
       self.city_name = o.get('cityName', '')
       self.hotel_id = o.get('hotelId', 0)
       self.hotel_name = o.get('hotelName', '')
       self.roomtype_id = o.get('roomTypeId', 0)
       self.roomtype_name = o.get('roomTypeName', '')
       self.rateplan_id = o.get('ratePlanId', 0)
       self.rateplan_name = o.get('ratePlanName', '')
       self.ota_id = o.get('otaId', 0)
       self.ota_order_id = o.get('otaOrderId', 0)
       self.ota_msg_desc = o.get('ota_msg_desc', '')
       self.currency_type = o.get('currencyType', 0)
       self.total_price = o.get('totalPrice', 0)
       self.price = o.get('price', 0)
       self.base_price = o.get('basePrice', 0)
       self.room_quantity = o.get('roomQuantity', 0)
       self.pay_type = o.get('payType', 0)
       self.bed_type = o.get('bedType', 0)
       self.bed_type_name = o.get('bedTypeName', '')
       self.checkin_date = o.get('checkInDate', '2014-12-24')
       self.checkout_date = o.get('checkOutDate', '2014-12-25')
       self.last_arrive_time = o.get('lastArriveTime', '18:00:00')
       self.contact_name = o.get('contactName', '')
       self.contact_mobile = o.get('contactMobile', '')
       self.contact_email = o.get('contactEmail', '')
       self.customer_quantity = o.get('customerQuantity', 0)
       self.customer_info = o.get('customerInfo', '')
       self.customer_remark = o.get('customerRemark', '')
       self.breakfast = o.get('breakfast', '')
       self.chain_id = o.get('chain_id', 0)
       self.chain_hotel_id = o.get('chainHotelId', 0)
       self.chain_roomtype_id = o.get('chainRoomTypeId', 0)
       self.chain_rateplan_id = o.get('chainRatePlanId', 0)
       self.chain_order_id = o.get('chainOrderId', 0)
       self.chain_total_price = o.get('chainTotalPrice', 0)
       self.confirmation_no = o.get('confirmationNo', 0)
       self.guarantee_info = o.get('guaranteeInfo', '')
       self.status = 0
       self.status_msg = o.get('statusMsg', '')
       self.extra = o.get('extra', '')
       self.merchant_id = 0

