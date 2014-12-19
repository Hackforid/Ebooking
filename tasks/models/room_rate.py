# -*- coding: utf-8 -*-


from tasks.celery_app import app
from tasks.base_task import SqlAlchemyTask

from models.room_rate import RoomRateModel
from exception.celery_exception import CeleryException

@app.task(base=SqlAlchemyTask, bind=True)
def new_roomrate(task_self, hotel_id, roomtype_id, rate_plan_id, commit=True):
    return RoomRateModel.new_roomrate(task_self.session, hotel_id, roomtype_id, rate_plan_id)

@app.task(base=SqlAlchemyTask, bind=True)
def set_price(self, id, price, start_date, end_date):
    roomrate = RoomRateModel.set_price(self.session, id, price, start_date, end_date)
    if roomrate:
        return roomrate
    else:
        return CeleryException(500, "修改失败")

