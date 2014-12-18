# -*- coding: utf-8 -*-


from tasks.celery_app import app
from tasks.base_task import SqlAlchemyTask

from models.rate_plan import RatePlanModel


@app.task(base=SqlAlchemyTask, bind=True)
def get_by_id(task_self, id):
    return task_self.session.query(RatePlanModel)\
            .filter(RatePlanModel.id == id)\
            .filter(RatePlanModel.is_delete == 0)\
            .first()

@app.task(base=SqlAlchemyTask, bind=True)
def new_rate_plan(task_self, merchant_id, hotel_id, roomtype_id, name, meal_type, punish_type):
    return RatePlanModel.new_rate_plan(task_self.session,
            merchant_id, hotel_id, roomtype_id, name, meal_type, punish_type)


@app.task(base=SqlAlchemyTask, bind=True)
def get_by_room(task_self, merchant_id, hotel_id, roomtype_id):
    return RatePlanModel.get_by_room(task_self.session, merchant_id, hotel_id, roomtype_id)
