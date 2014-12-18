# -*- coding: utf-8 -*-


from tasks.celery_app import app
from tasks.base_task import SqlAlchemyTask

from models.cooperate_hotel import CooperateHotelModel



@app.task(base=SqlAlchemyTask, bind=True)
def get_by_id(task_self, id):
    return CooperateHotelModel.get_by_id(task_self.session, id)

@app.task(base=SqlAlchemyTask, bind=True)
def get_by_merchant_id(task_self, merchant_id):
    return CooperateHotelModel.get_by_merchant_id(task_self.session, merchant_id)

@app.task(base=SqlAlchemyTask, bind=True)
def get_by_merchant_id_and_hotel_id(task_self, merchant_id, hotel_id):
    return CooperateHotelModel.get_by_merchant_id_and_hotel_id(task_self.session, merchant_id, hotel_id)

@app.task(base=SqlAlchemyTask, bind=True)
def new_hotel_cooprate(task_self, merchant_id, hotel_id):
    coop = CooperateHotelModel.new_hotel_cooprate(task_self.session, merchant_id, hotel_id)
    coop.id
    return coop

@app.task(base=SqlAlchemyTask, bind=True)
def delete_hotel_cooprate(task_self, merchant_id, hotel_id):
    coop = CooperateHotelModel.delete_hotel_cooprate(task_self.session, merchant_id, hotel_id)
    print 'delete hotel coop', coop.id
    return coop
