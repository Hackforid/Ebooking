# -*- coding: utf-8 -*-

import datetime


from tasks.celery_app import app
from tasks.base_task import SqlAlchemyTask
from tasks.stock import PushHotelTask, PushInventoryTask
from models.cooperate_roomtype import CooperateRoomTypeModel
from models.inventory import InventoryModel
from models.cooperate_hotel import CooperateHotelModel
from exception.celery_exception import CeleryException


@app.task(base=SqlAlchemyTask, bind=True)
def get_by_hotel_id(task_self, hotel_id):
    return CooperateRoomTypeModel.get_by_hotel_id(task_self.session, hotel_id)

@app.task(base=SqlAlchemyTask, bind=True)
def get_by_merchant_id_and_hotel_id(task_self, merchant_id, hotel_id):
    return CooperateRoomTypeModel.get_by_merchant_id_and_hotel_id(task_self.session, merchant_id, hotel_id)


@app.task(base=SqlAlchemyTask, bind=True)
def new_roomtype_coops(task_self, merchant_id, hotel_id, roomtype_ids):
    hotel = CooperateHotelModel.get_by_id(task_self.session, hotel_id)
    if not hotel:
        raise CeleryException(1000, 'hotel not found')
    if hotel.merchant_id != merchant_id:
        raise CeleryException(2000, 'merchant not valid')


    coops = CooperateRoomTypeModel.get_by_merchant_hotel_base_rooms_id(task_self.session,
            merchant_id, hotel_id, roomtype_ids)
    if coops:
        raise CeleryException(1000, 'room has cooped')

    coops = CooperateRoomTypeModel.new_roomtype_coops(task_self.session,
            merchant_id, hotel.id,  hotel.base_hotel_id, roomtype_ids)

    for coop in coops:
        InventoryModel.insert_in_four_month(task_self.session,
                merchant_id, hotel_id, coop.id, hotel.base_hotel_id, coop.base_roomtype_id)

    PushHotelTask().push_hotel.delay(hotel_id)
    for coop in coops:
        PushInventoryTask().push_inventory(coop.id)
        create_default_rateplan(coop)

    return coops

def create_default_rateplan(coop_room):
    from tasks.models.rate_plan import new_rate_plan
    new_rate_plan.delay(coop_room.merchant_id, coop_room.hotel_id, coop_room.id, "常规价格", 0, 0)


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
    coop = CooperateRoomTypeModel.get_by_id(self.session, roomtype_id)
    if not coop:
        return CeleryException(404, 'coop not found')
    if coop.merchant_id != merchant_id:
        return CeleryException(1000, 'merchant not valid')

    coop.prefix_name = prefix_name
    coop.remark_name = remark_name
    self.session.commit()

    return coop


@app.task(base=SqlAlchemyTask, bind=True)
def check_inventories(self):
    cooped_rooms = CooperateRoomTypeModel.get_all(self.session)
    cooped_room_ids = [room.id for room in cooped_rooms]


    #dates = InventoryModel.get_months(4)
    #months = [InventoryModel.combin_year_month(date[0], date[1]) for date in dates]
    #inventories = InventoryModel.get_by_room_ids_and_months(session, cooped_room_ids, months)
    #need_complete_roomtype_ids = []
    #for room in cooped_rooms:
        #for month in months:
            #for inventory in inventories:
                #if inventory.roomtype_id == room.roomtype_id and inventory.hotel_id = room.hotel_id and ivnentory.merchant_id Periodic Task and inventory.month == month:
                    #break
            #else:
                #need_complete_roomtype_ids.append(roomtype_id)

