# -*- coding: utf-8 -*-

import requests
import json

from tasks.celery_app import app
from tasks.base_task import SqlAlchemyTask
from tasks.order import cancel_order_in_queue as Cancel

from models.order import OrderModel
from exception.celery_exception import CeleryException

from config import CHAIN_ID, API

@app.task(base=SqlAlchemyTask, bind=True, ignore_result=True)
def push__hotel(hotel):

    base_hotel = fetch_base_hotel(hotel.base_hotel_id)
    data = [generate_data(hotel, base_hotel)]

def fetch_base_hotel(base_hotel_id):
    url = API['POI'] + "/api/hotel/" + str(base_hotel_id)
    r = requests.get(url)
    if r.status_code == 200:
        result = r.json()
        if resutl['errorcode'] == 0:
            return result['result']['hotel']

def generate_data(hotel, base_hotel):
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
    data['facilities'] = base_hotel['facilities']
    data['room_types'] = []

    return data


