# -*- coding: utf-8 -*-

from tornado.escape import json_encode, json_decode

from views.base import BtwBaseHandler
from models.merchant import MerchantModel 
from models.cooperate_hotel import CooperateHotelModel as Hotel

class MerchantListAPIHandler(BtwBaseHandler):

    def get(self):
        merchants = MerchantModel.get_all(self.db)
        self.finish_json(result=dict(
            merchants=[merchant.todict() for merchant in merchants]
            ))

class MerchantQueryByHotelAPIHandler(BtwBaseHandler):

    def get(self, hotel_id):
            hotel = Hotel.get_by_id(self.db, hotel_id)
            if hotel:
                merchant = MerchantModel.get_by_id(self.db, hotel.merchant_id)
                if merchant:
                    self.finish_json(result=dict(
                        merchant=merchant.todict()))
                    return

            self.finish_json(result=dict(
                merchant={}))
