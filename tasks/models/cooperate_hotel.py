# -*- coding: utf-8 -*-


from tasks.celery_app import app
from tasks.base_task import SqlAlchemyTask

from models.cooperate_hotel import CooperateHotelModel
from exception.celery_exception import CeleryException


@app.task(base=SqlAlchemyTask, bind=True)
def get_by_id(task_self, id):
    return CooperateHotelModel.get_by_id(task_self.session, id)

@app.task(base=SqlAlchemyTask, bind=True)
def get_by_merchant_id(task_self, merchant_id):
    return CooperateHotelModel.get_by_merchant_id(task_self.session, merchant_id)

@app.task(base=SqlAlchemyTask, bind=True)
def new_hotel_cooprate(self, merchant_id, hotel_id):
    coop = CooperateHotelModel.get_by_merchant_id_and_base_hotel_id(self.session, merchant_id, hotel_id)
    if coop:
        raise CeleryException(1000, u'已经合作')

    coop = CooperateHotelModel.new_hotel_cooprate(self.session, merchant_id, hotel_id)
    return coop

