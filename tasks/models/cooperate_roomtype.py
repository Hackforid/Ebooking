# -*- coding: utf-8 -*-

import datetime


from tasks.celery_app import app
from tasks.base_task import SqlAlchemyTask
from models.cooperate_roomtype import CooperateRoomTypeModel
from models.inventory import InventoryModel
from models.cooperate_hotel import CooperateHotelModel
from exception.celery_exception import CeleryException



@app.task(base=SqlAlchemyTask, bind=True)
def get_by_merchant_id_and_hotel_id(task_self, merchant_id, hotel_id):
    return CooperateRoomTypeModel.get_by_merchant_id_and_hotel_id(task_self.session, merchant_id, hotel_id)


@app.task(base=SqlAlchemyTask, bind=True)
def new_roomtype_coops(task_self, merchant_id, hotel_id, roomtype_ids):
    hotel = CooperateHotelModel.get_by_merchant_id_and_hotel_id(task_self.session, merchant_id, hotel_id)
    if not hotel:
        raise CeleryException(1000, 'hotel not found')


    coops = CooperateRoomTypeModel.get_by_merchant_hotel_rooms_id(task_self.session,
            merchant_id, hotel_id, roomtype_ids)
    if coops:
        raise CeleryException(1000, 'room has cooped')

    coops = CooperateRoomTypeModel.new_roomtype_coops(task_self.session,
            merchant_id, hotel_id, roomtype_ids)

    for coop in coops:
        InventoryModel.insert_in_four_month(task_self.session,
                merchant_id, hotel_id, coop.roomtype_id)

    return coops

@app.task(base=SqlAlchemyTask, bind=True)
def modify_cooped_roomtype_online(self, merchant_id, hotel_id, roomtype_id, is_online):
    coop = CooperateRoomTypeModel.get_by_merchant_hotel_room_id(self.session,
            merchant_id, hotel_id, roomtype_id)
    if not coop:
        return CeleryException(404, 'coop not found')

    coop.is_online = is_online
    self.session.commit()

    return coop

@app.task(base=SqlAlchemyTask, bind=True)
def modify_cooped_roomtype(self, merchant_id, hotel_id, roomtype_id, prefix_name, remark_name):
    coop = CooperateRoomTypeModel.get_by_merchant_hotel_room_id(self.session,
            merchant_id, hotel_id, roomtype_id)
    if not coop:
        return CeleryException(404, 'coop not found')

    coop.prefix_name = prefix_name
    coop.remark_name = remark_name
    self.session.commit()

    return coop
