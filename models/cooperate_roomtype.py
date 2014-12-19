# -*- coding: utf-8 -*-

import datetime

from tornado.util import ObjectDict 

from tasks.models import Base
from sqlalchemy import Column
from sqlalchemy.dialects.mysql import BIT, INTEGER, VARCHAR, DATETIME, BIGINT


class CooperateRoomTypeModel(Base):

    __tablename__ = 'cooperateRoomType'
    __table_args__ = {
        'mysql_charset': 'utf8', 'mysql_engine': 'InnoDB'}


    id = Column(INTEGER, primary_key=True, autoincrement=True)
    merchant_id = Column("merchantId", INTEGER, nullable=False, default=0)
    hotel_id = Column("hotelId", INTEGER, nullable=False, default=0)
    roomtype_id = Column("roomTypeId", INTEGER, nullable=False, default=0)
    is_online = Column('isOnline', BIT, nullable=False, default=0)
    is_delete = Column('isDelete', BIT, nullable=False, default=0)

    @classmethod
    def get_by_id(cls, session, id):
        return session.query(CooperateRoomTypeModel)\
                .filter(CooperateRoomTypeModel.id == id)\
                .filter(CooperateRoomTypeModel.is_delete == 0)\
                .first()

    @classmethod
    def get_by_merchant_id_and_hotel_id(cls, session, merchant_id, hotel_id):
        return session.query(CooperateRoomTypeModel)\
                .filter(CooperateRoomTypeModel.merchant_id == merchant_id)\
                .filter(CooperateRoomTypeModel.hotel_id == hotel_id)\
                .filter(CooperateRoomTypeModel.is_delete == 0)\
                .all()

    @classmethod
    def get_by_merchant_hotel_room_id(cls, session, merchant_id, hotel_id, roomtype_id):
        return session.query(CooperateRoomTypeModel)\
                .filter(CooperateRoomTypeModel.merchant_id == merchant_id)\
                .filter(CooperateRoomTypeModel.hotel_id == hotel_id)\
                .filter(CooperateRoomTypeModel.roomtype_id == roomtype_id)\
                .filter(CooperateRoomTypeModel.is_delete == 0)\
                .first()

    @classmethod
    def new_roomtype_coops(cls, session, merchant_id, hotel_id, roomtype_ids):
        coops = []
        try:

            for roomtype_id in roomtype_ids:
                coop = CooperateRoomTypeModel(merchant_id=merchant_id, hotel_id=hotel_id, roomtype_id=roomtype_id)
                coops.append(coop)

            session.add_all(coops)
            session.commit()
        except:
            session.rollback()
            return

        from models.inventory import InventoryModel
        toyear = datetime.date.today().year
        for roomtype_id in roomtype_ids:
            InventoryModel.insert_by_year(session, merchant_id, hotel_id, roomtype_id, toyear)

        return coops

    def todict(self):
        return ObjectDict(
                id = self.id,
                merchant_id = self.merchant_id,
                hotel_id = self.hotel_id,
                roomtype_id = self.roomtype_id,
                is_online = self.is_online,
                )

