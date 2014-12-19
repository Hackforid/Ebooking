# -*- coding: utf-8 -*-


from tasks.celery_app import app
from tasks.base_task import SqlAlchemyTask

from models.rate_plan import RatePlanModel
from models.room_rate import RoomRateModel

from exception.celery_exception import CeleryException


@app.task(base=SqlAlchemyTask, bind=True)
def get_by_id(task_self, id):
    return task_self.session.query(RatePlanModel)\
            .filter(RatePlanModel.id == id)\
            .filter(RatePlanModel.is_delete == 0)\
            .first()

@app.task(base=SqlAlchemyTask, bind=True)
def new_rate_plan(task_self, merchant_id, hotel_id, roomtype_id, name, meal_type, punish_type):
    rate_plan = RatePlanModel.get_by_merchant_hotel_room_name(task_self.session, merchant_id, hotel_id, roomtype_id, name)
    if rate_plan:
        return CeleryException(errcode=405, errmsg="name exist")

    return RatePlanModel.new_rate_plan(task_self.session,
            merchant_id, hotel_id, roomtype_id, name, meal_type, punish_type)


@app.task(base=SqlAlchemyTask, bind=True)
def get_by_room(task_self, merchant_id, hotel_id, roomtype_id):
    return RatePlanModel.get_by_room(task_self.session, merchant_id, hotel_id, roomtype_id)

@app.task(base=SqlAlchemyTask, bind=True)
def modify_rateplan(self, rateplan_id, name, meal_num, punish_type):
    rateplan = RatePlanModel.get_by_id(self.session, rateplan_id)
    if not rateplan:
        return CeleryException(errcode=404, errmsg="rateplan not found")

    _rateplan = RatePlanModel.get_by_merchant_hotel_room_name(self.session,
            rateplan.merchant_id, rateplan.hotel_id, rateplan.roomtype_id, name)
    if _rateplan and _rateplan.id != rateplan.id:
        return CeleryException(errcode=405, errmsg="name exist")

    rateplan.name = name
    rateplan.punish_type = punish_type

    roomrate =RoomRateModel.set_meal(self.session, rateplan.id, meal_num, False)

    self.session.commit()

    return rateplan, roomrate







