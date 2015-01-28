# -*- coding: utf-8 -*-


from tasks.celery_app import app
from tasks.base_task import SqlAlchemyTask
from tasks.stock import PushHotelTask
from tasks.poi import POIPushHotelTask

from models.cooperate_hotel import CooperateHotelModel
from exception.celery_exception import CeleryException


@app.task(base=SqlAlchemyTask, bind=True)
def get_by_id(task_self, id):
    return CooperateHotelModel.get_by_id(task_self.session, id)

@app.task(base=SqlAlchemyTask, bind=True)
def get_by_merchant_id(task_self, merchant_id, is_online=None):
    return CooperateHotelModel.get_by_merchant_id(task_self.session, merchant_id, is_online)

@app.task(base=SqlAlchemyTask, bind=True)
def new_hotel_cooprate(self, merchant_id, hotel_id):
    coop = CooperateHotelModel.get_by_merchant_id_and_base_hotel_id(self.session, merchant_id, hotel_id)
    if coop:
        raise CeleryException(1000, u'已经合作')

    coop = CooperateHotelModel.new_hotel_cooprate(self.session, merchant_id, hotel_id)

    PushHotelTask().push_hotel.delay(coop.id)
    POIPushHotelTask().push_hotel.delay(coop.id)

    return coop

@app.task(base=SqlAlchemyTask, bind=True)
def new_hotel_cooprates(self, merchant_id, hotel_ids):
    coops = CooperateHotelModel.new_hotel_cooprates(self.session, merchant_id, hotel_ids)
    for coop in coops:
        POIPushHotelTask().push_hotel.delay(coop.id)
    return coops

@app.task(base=SqlAlchemyTask, bind=True)
def change_hotel_online_status(self, merchant_id, hotel_id, is_online):
    hotel = CooperateHotelModel.get_by_merchant_id_and_hotel_id(self.session, merchant_id, hotel_id)
    if not hotel:
        raise CeleryException(404, 'hotel not found')

    hotel.is_online = is_online
    self.session.commit()

    PushHotelTask().push_hotel.delay(hotel.id)
    return hotel
