# -*- coding: utf-8 -*-

from __future__ import absolute_import

import requests
import traceback

from celery.contrib.methods import task_method

from tasks.celery_app import app
from tasks.base_task import SqlAlchemyTask

from tools.json import json_encode
from tools.log import Log
from config import API, IS_PUSH_TO_POI

class POIPushHotelTask(SqlAlchemyTask):

    @app.task(filter=task_method, ignore_result=True)
    def push_hotel(self, hotel_id):
        Log.info("<<POI push hotel mapping {}>> start".format(hotel_id))
        if not IS_PUSH_TO_POI:
            return


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
        Log.info(u"<<POI push hotel mapping>> push request {}".format(hotel_data))
        url = API['POI'] + '/api/push/ebooking/hotel/'
        r = requests.post(url, data=json_encode(hotel_data))
        Log.info("<<POI push hotel mapping>> response {}".format(r.text))

class POIPushRoomTypeTask(SqlAlchemyTask):

    @app.task(filter=task_method, ignore_result=True)
    def push_roomtype(self, roomtype_id):
        Log.info("<<POI push room mapping {}>> start".format(roomtype_id))
        if not IS_PUSH_TO_POI:
            return
        from models.cooperate_roomtype import CooperateRoomTypeModel

        room = CooperateRoomTypeModel.get_by_id(self.session, roomtype_id)
        if not room:
            Log.error("no roomtype")
            return

        room_data = self.generate_data(room)
        self.post_room(room_data)


    def generate_data(self, room):
        data = {}
        data['chain_hotel_id'] = room.hotel_id
        data['chain_roomtype_id'] = room.id
        data['main_roomtype_id'] = room.base_roomtype_id
        return data
        
    def post_room(self, room_data):
        Log.info(u"<<POI push roomtype mapping>> push request {}".format(room_data))
        url = API['POI'] + '/api/push/ebooking/room/'
        r = requests.post(url, data=json_encode(room_data))
        Log.info("<<POI push roomtype mapping>> response {}".format(r.text))

class POIPushTask(SqlAlchemyTask):

    @app.task(filter=task_method, ignore_result=True)
    def push_all(self):
        Log.info("<<POI push all>> start")
        if not IS_PUSH_TO_POI:
            return

        from models.merchant import MerchantModel
        merchants = MerchantModel.get_all(self.session)
        for merchant in merchants:
            try:
                self.push_by_merchant(merchant)
            except Exception as e:
                Log.debug(traceback.format_exc())

    def push_by_merchant(self, merchant):
        from models.cooperate_hotel import CooperateHotelModel
        hotels =  CooperateHotelModel.get_by_merchant_id(self.session, merchant.id)

        self.push_hotels(merchant, hotels)
        for hotel in hotels:
            self.push_room_by_hotel(merchant, hotel)


    def push_hotels(self, merchant, hotels):
        hotel_datas = [self.generate_hotel_data(merchant, hotel) for hotel in hotels]
        self.post_hotels(hotel_datas)

    def generate_hotel_data(self, merchant, hotel):
        data = {}
        data['chain_hotel_id'] = hotel.id
        data['main_hotel_id'] = hotel.base_hotel_id
        data['merchant_id'] = hotel.merchant_id
        data['merchant_name'] = merchant.name
        return data

    def post_hotels(self, hotel_datas):
        data = {'hotels': hotel_datas}
        Log.info(u"<<POI push hotel mapping>> push request {}".format(data))
        url = API['POI'] + '/api/push/ebooking/hotels/'
        r = requests.post(url, json=data)
        Log.info("<<POI push hotel mapping>> response {}".format(r.text))

    def push_room_by_hotel(self, merchant, hotel):
        from models.cooperate_roomtype import CooperateRoomTypeModel
        roomtypes = CooperateRoomTypeModel.get_by_hotel_id(self.session, hotel.id)
        room_datas = [self.generate_room_data(roomtype) for roomtype in roomtypes]
        self.post_room(room_datas)

    def generate_room_data(self, roomtype):
        data = {}
        data['chain_hotel_id'] = roomtype.hotel_id
        data['chain_roomtype_id'] = roomtype.id
        data['main_roomtype_id'] = roomtype.base_roomtype_id
        return data
        
    def post_room(self, room_datas):
        data = {'roomtypes': room_datas}
        Log.info(u"<<POI push roomtype mapping>> push request {}".format(data))
        url = API['POI'] + '/api/push/ebooking/rooms/'
        r = requests.post(url, json=data)
        Log.info("<<POI push roomtype mapping>> response {}".format(r.text))



@app.task(base=SqlAlchemyTask, bind=True, ignore_result=True)
def push_poi(self):
    Log.info('push all to poi')
    POIPushTask().push_all.delay()
