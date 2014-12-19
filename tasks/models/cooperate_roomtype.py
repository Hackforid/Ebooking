# -*- coding: utf-8 -*-

import datetime


from tasks.celery_app import app
from tasks.base_task import SqlAlchemyTask
from models.cooperate_roomtype import CooperateRoomTypeModel
from exception.celery_exception import CeleryException



@app.task(base=SqlAlchemyTask, bind=True)
def get_by_merchant_id_and_hotel_id(task_self, merchant_id, hotel_id):
    return CooperateRoomTypeModel.get_by_merchant_id_and_hotel_id(task_self.session, merchant_id, hotel_id)


@app.task(base=SqlAlchemyTask, bind=True)
def new_roomtype_coops(task_self, merchant_id, hotel_id, roomtype_ids):
    return CooperateRoomTypeModel.new_roomtype_coops(task_self.session,
            merchant_id, hotel_id, roomtype_ids)


@app.task(base=SqlAlchemyTask, bind=True)
def modify_cooped_roomtype(self, merchant_id, hotel_id, roomtype_id, is_online):
    coop = CooperateRoomTypeModel.get_by_merchant_hotel_room_id(self.session,
            merchant_id, hotel_id, roomtype_id)
    if not coop:
        return CeleryException(404, 'coop not found')

    coop.is_online = is_online
    self.session.commit()

    return coop

