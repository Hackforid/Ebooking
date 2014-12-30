# -*- coding: utf-8 -*-

import datetime
import traceback

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
    base_hotel_id = Column("baseHotelId", INTEGER, nullable=False, default=0)
    base_roomtype_id = Column("baseRoomTypeId", INTEGER, nullable=False, default=0)
    is_online = Column('isOnline', BIT, nullable=False, default=1)
    is_delete = Column('isDelete', BIT, nullable=False, default=0)
    prefix_name = Column('prefixName', VARCHAR(100))
    remark_name = Column('remarkName', VARCHAR(100))

    @classmethod
    def get_all(cls, session):
        return session.query(CooperateRoomTypeModel)\
                .filter(CooperateRoomTypeModel.is_delete == 0)\
                .all()

    @classmethod
    def get_all_ids(cls, session):
        return session.query(CooperateRoomTypeModel.id)\
                .filter(CooperateRoomTypeModel.is_delete == 0)\
                .all()

    @classmethod
    def get_by_id(cls, session, id):
        return session.query(CooperateRoomTypeModel)\
                .filter(CooperateRoomTypeModel.id == id)\
                .filter(CooperateRoomTypeModel.is_delete == 0)\
                .first()

    @classmethod
    def get_by_hotel_id(cls, session, hotel_id):
        return session.query(CooperateRoomTypeModel)\
                .filter(CooperateRoomTypeModel.hotel_id == hotel_id)\
                .filter(CooperateRoomTypeModel.is_delete == 0)\
                .all()

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
                .filter(CooperateRoomTypeModel.base_roomtype_id == roomtype_id)\
                .filter(CooperateRoomTypeModel.is_delete == 0)\
                .first()

    @classmethod
    def get_by_merchant_hotel_base_rooms_id(cls, session, merchant_id, hotel_id, base_roomtype_ids):
        return session.query(CooperateRoomTypeModel)\
                .filter(CooperateRoomTypeModel.merchant_id == merchant_id)\
                .filter(CooperateRoomTypeModel.hotel_id == hotel_id)\
                .filter(CooperateRoomTypeModel.base_roomtype_id.in_(base_roomtype_ids))\
                .filter(CooperateRoomTypeModel.is_delete == 0)\
                .all()

    @classmethod
    def new_roomtype_coops(cls, session, merchant_id, hotel_id, base_hotel_id, base_roomtype_ids):
        coops = []
        try:

            for roomtype_id in base_roomtype_ids:
                coop = CooperateRoomTypeModel(merchant_id=merchant_id, hotel_id=hotel_id, base_roomtype_id=roomtype_id, base_hotel_id=base_hotel_id)
                coops.append(coop)

            session.add_all(coops)
            session.commit()
        except:
            print traceback.format_exc()
            session.rollback()
            return
        return coops

    def todict(self):
        return ObjectDict(
                id = self.id,
                merchant_id = self.merchant_id,
                base_hotel_id=self.base_hotel_id,
                hotel_id = self.hotel_id,
                base_roomtype_id = self.base_roomtype_id,
                is_online = self.is_online,
                prefix_name = self.prefix_name,
                remark_name = self.remark_name,
                )

