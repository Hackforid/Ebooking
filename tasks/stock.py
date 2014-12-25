# -*- coding: utf-8 -*-

import requests
import json
import time

from tasks.celery_app import app
from tasks.base_task import SqlAlchemyTask
from tasks.order import cancel_order_in_queue as Cancel

from models.order import OrderModel
from models.cooperate_roomtype import CooperateRoomTypeModel
from exception.celery_exception import CeleryException

from config import CHAIN_ID, API

@app.task(base=SqlAlchemyTask, bind=True, ignore_result=True)
def push_hotel(self, hotel_id):
    from models.cooperate_hotel import CooperateHotelModel

    hotel = CooperateHotelModel.get_by_id(self.session, hotel_id)
    if not hotel:
        return

    roomtypes = CooperateRoomTypeModel.get_by_hotel_id(self.session, hotel_id)

    base_hotel, base_roomtypes = fetch_base_hotel_and_roomtypes(hotel.base_hotel_id)
    if not base_hotel:
        return

    hotel_data = generate_data(hotel, roomtypes, base_hotel, base_roomtypes)
    post_hotel(hotel_data)

def post_hotel(hotel_data):
    track_id = generate_track_id(hotel_data['id'])
    data = {'list': [hotel_data]}
    params = {'track_id': track_id, 'data': json.dumps(data)}
    print params
    url = API['STOCK'] + '/stock/update_hotel'
    r = requests.post(url, data=params)
    print r.text

def generate_track_id(hotel_id):
    return "{}|{}".format(hotel_id, time.time())

def fetch_base_hotel(base_hotel_id):
    url = API['POI'] + "/api/hotel/" + str(base_hotel_id)
    r = requests.get(url)
    if r.status_code == 200:
        result = r.json()
        if result['errorcode'] == 0:
            return result['result']['hotel']

def generate_data(hotel, roomtypes, base_hotel, base_roomtypes):
    data = {}
    data['chain_id'] = CHAIN_ID
    data['id'] = hotel.id
    data['name'] = base_hotel['name']
    data['is_valid'] = hotel.is_online
    data['city_id'] = base_hotel['city_id']
    data['district_id'] = base_hotel['district_id']
    data['address'] = base_hotel['address']
    data['star'] = base_hotel['star']
    data['tel'] = base_hotel['phone']
    data['facilities'] = base_hotel['facilities'].replace(',', '|') if base_hotel['facilities'] else ''
    data['room_types'] = generate_rooms(roomtypes, base_roomtypes)

    return data

def generate_rooms(roomtypes, base_roomtypes):
    rooms = []
    for roomtype in roomtypes:
        for base_roomtype in base_roomtypes:
            if base_roomtype['id'] == roomtype.base_roomtype_id:
                room = {}
                room['id'] = roomtype.id
                room['name'] = base_roomtype['name']
                room['bed_type'] = base_roomtype['bed_type']
                room['facilities'] = base_roomtype['facilities'].replace(',', '|') if base_roomtype['facilities'] else ''
                rooms.append(room)
                break
    return rooms



def fetch_base_hotel_and_roomtypes(hotel_id):
    url = API['POI'] + "/api/hotel/" + str(hotel_id) + "/roomtype/"
    r = requests.get(url)
    if r.status_code == 200:
        result = r.json()
        if result['errcode'] == 0:
            return result['result']['hotel'], result['result']['roomtypes']

    return None, None

