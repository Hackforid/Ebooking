# -*- coding: utf-8 -*-

import datetime


from tasks.celery_app import app
from tasks.base_task import SqlAlchemyTask
from models.cooperate_roomtype import CooperateRoomTypeModel



@app.task(base=SqlAlchemyTask, bind=True)
def get_by_merchant_id_and_hotel_id(task_self, merchant_id, hotel_id):
    return CooperateRoomTypeModel.get_by_merchant_id_and_hotel_id(task_self.session, merchant_id, hotel_id)


@app.task(base=SqlAlchemyTask, bind=True)
def new_roomtype_coops(task_self, merchant_id, hotel_id, roomtype_ids):
    return CooperateRoomTypeModel.new_roomtype_coops(task_self.session,
            merchant_id, hotel_id, roomtype_ids)
