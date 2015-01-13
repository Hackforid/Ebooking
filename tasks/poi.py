# -*- coding: utf-8 -*-

import requests
import json
import time
import datetime

from celery.contrib.methods import task_method

from tasks.celery_app import app
from tasks.base_task import SqlAlchemyTask

from exception.celery_exception import CeleryException
from tools.json import json_encode
from tools.log import Log
from config import CHAIN_ID, API

class PushHotelTask(SqlAlchemyTask):

    @app.task(filter=task_method, ignore_result=True)
    def push_hotel(self, hotel_id):
        Log.info("<<POI push hotel mapping {}>> start".format(hotel_id))
        from models.cooperate_hotel import CooperateHotelModel
        from models.merchant import MerchantModel

        hotel = CooperateHotelModel.get_by_id(self.session, hotel_id)
        if not hotel:
            return
        merchant = MerchantModel.get_by_id(self.session, hotel.merchant_id)
        if not merchant:
            return

        hotel_data = self.generate_data(hotel, merchant)
        self.post_hotel(hotel_data)

    def generate_data(self, hotel, merchant):
        data = {}
        data['chain_hotel_id'] = hotel.id
        data['main_hotel_id'] = hotel.base_hotel_id
        data['merchant_id'] = hotel.merchant_id
        data['merchant_name'] = merchant.name
        return data

    def post_hotel(self, hotel_data):
        Log.info(u"<<push hotel>> push request {}".format(hotel_data))
        url = API['POI'] + '/stock/update_hotel'
        r = requests.post(url, json=hotel_data)
        Log.info("<<push hotel>> response {}".format(r.text))

