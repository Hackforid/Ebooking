# -*- coding: utf-8 -*-


from tasks.celery_app import app
from tasks.base_task import SqlAlchemyTask
from tasks.stock import PushRatePlanTask

from models.rate_plan import RatePlanModel
from models.room_rate import RoomRateModel
from models.cooperate_roomtype import CooperateRoomTypeModel

from exception.celery_exception import CeleryException


@app.task(base=SqlAlchemyTask, bind=True)
def get_by_id(task_self, id):
    return task_self.session.query(RatePlanModel)\
        .filter(RatePlanModel.id == id)\
        .filter(RatePlanModel.is_delete == 0)\
        .first()


@app.task(base=SqlAlchemyTask, bind=True)
def new_rate_plan(self, merchant_id, hotel_id, roomtype_id, name, meal_num, punish_type):
    room = CooperateRoomTypeModel.get_by_id(self.session, roomtype_id)
    if not room:
        raise CeleryException(errcode=404, errmsg='room not exist')

    rate_plan = RatePlanModel.get_by_merchant_hotel_room_name(
        self.session, merchant_id, hotel_id, roomtype_id, name)
    if rate_plan:
        raise CeleryException(errcode=405, errmsg="name exist")

    new_rateplan = RatePlanModel.new_rate_plan(self.session,
        merchant_id, hotel_id, roomtype_id, room.base_hotel_id, room.base_roomtype_id,  name, meal_num, punish_type)
    new_roomrate = RoomRateModel.new_roomrate(self.session, hotel_id, roomtype_id, room.base_hotel_id, room.base_roomtype_id, new_rateplan.id, meal_num)

    PushRatePlanTask().push_rateplan.delay(new_rateplan.id)
    print new_rateplan, new_roomrate
    return new_rateplan, new_roomrate


@app.task(base=SqlAlchemyTask, bind=True)
def get_by_room(task_self, merchant_id, hotel_id, roomtype_id):
    rateplans = RatePlanModel.get_by_room(task_self.session, merchant_id, hotel_id, roomtype_id)
    rateplan_ids = [rateplan.id for rateplan in rateplans]
    roomrates= RoomRateModel.get_by_rateplans(task_self.session, rateplan_ids)
    return rateplans, roomrates

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

    roomrate = RoomRateModel.set_meal(
        self.session, rateplan.id, meal_num, False)

    self.session.commit()

    PushRatePlanTask().push_rateplan.delay(rateplan.id, with_roomrate=True)
    return rateplan, roomrate
