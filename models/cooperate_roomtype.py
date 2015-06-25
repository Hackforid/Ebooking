# -*- coding: utf-8 -*-

import traceback

from tornado.util import ObjectDict 

from models import Base
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
        ids = session.query(CooperateRoomTypeModel.id)\
                .filter(CooperateRoomTypeModel.is_delete == 0)\
                .all()
        return [id for id, in ids]

    @classmethod
    def get_by_id(cls, session, id):
        return session.query(CooperateRoomTypeModel)\
                .filter(CooperateRoomTypeModel.id == id)\
                .filter(CooperateRoomTypeModel.is_delete == 0)\
                .first()

    @classmethod
    def get_by_ids(cls, session, ids, with_delete=False):
        query = session.query(CooperateRoomTypeModel)\
                .filter(CooperateRoomTypeModel.id.in_(ids))
        if not with_delete:
            query = query.filter(CooperateRoomTypeModel.is_delete == 0)
        return query.all()

    @classmethod
    def get_by_hotel_id(cls, session, hotel_id, with_delete=False):
        query = session.query(CooperateRoomTypeModel)\
                .filter(CooperateRoomTypeModel.hotel_id == hotel_id)
        if not with_delete:
            query = query.filter(CooperateRoomTypeModel.is_delete == 0)
        return query.all()

    @classmethod
    def get_by_hotel_ids(cls, session, hotel_ids, with_delete=False):
        query = session.query(CooperateRoomTypeModel)\
                .filter(CooperateRoomTypeModel.hotel_id.in_(hotel_ids))
        if not with_delete:
            query = query.filter(CooperateRoomTypeModel.is_delete == 0)
        return query.all() 

    @classmethod
    def get_by_merchant_id_and_hotel_id(cls, session, merchant_id, hotel_id):
        return session.query(CooperateRoomTypeModel)\
                .filter(CooperateRoomTypeModel.merchant_id == merchant_id)\
                .filter(CooperateRoomTypeModel.hotel_id == hotel_id)\
                .filter(CooperateRoomTypeModel.is_delete == 0)\
                .all()

    @classmethod
    def get_by_merchant_hotel_and_id(cls, session, merchant_id, hotel_id, id):
        return session.query(CooperateRoomTypeModel)\
                .filter(CooperateRoomTypeModel.merchant_id == merchant_id)\
                .filter(CooperateRoomTypeModel.hotel_id == hotel_id)\
                .filter(CooperateRoomTypeModel.id == id)\
                .filter(CooperateRoomTypeModel.is_delete == 0)\
                .first()

    @classmethod
    def get_by_merchant_hotel_room_id(cls, session, merchant_id, hotel_id, roomtype_id, with_delete=False):
        query = session.query(CooperateRoomTypeModel)\
                .filter(CooperateRoomTypeModel.merchant_id == merchant_id)\
                .filter(CooperateRoomTypeModel.hotel_id == hotel_id)\
                .filter(CooperateRoomTypeModel.base_roomtype_id == roomtype_id)
        if not with_delete:
            query = query.filter(CooperateRoomTypeModel.is_delete == 0)

        return query.first()

    @classmethod
    def get_by_merchant_hotel_base_rooms_id(cls, session, merchant_id, hotel_id, base_roomtype_ids):
        return session.query(CooperateRoomTypeModel)\
                .filter(CooperateRoomTypeModel.merchant_id == merchant_id)\
                .filter(CooperateRoomTypeModel.hotel_id == hotel_id)\
                .filter(CooperateRoomTypeModel.base_roomtype_id.in_(base_roomtype_ids))\
                .filter(CooperateRoomTypeModel.is_delete == 0)\
                .all()

    @classmethod
    def get_by_merchant_id(cls, session, merchant_id):
        return session.query(CooperateRoomTypeModel)\
                .filter(CooperateRoomTypeModel.merchant_id == merchant_id)\
                .filter(CooperateRoomTypeModel.is_delete == 0)\
                .all()

    @classmethod
    def new_roomtype_coops(cls, session, merchant_id, hotel_id, base_hotel_id, base_roomtype_ids, commit=True):
        coops = []
        try:
            for roomtype_id in base_roomtype_ids:
                coop = cls.get_by_merchant_hotel_room_id(session, merchant_id, hotel_id, roomtype_id, with_delete=True)
                if coop:
                    coop.is_delete = 0
                else:
                    coop = CooperateRoomTypeModel(merchant_id=merchant_id, hotel_id=hotel_id, base_roomtype_id=roomtype_id, base_hotel_id=base_hotel_id)
                coops.append(coop)

            session.add_all(coops)
            if commit:
                session.commit()
            else:
                session.flush()
        except:
            print traceback.format_exc()
            session.rollback()
            return
        return coops

    @classmethod
    def set_online_by_merchant(cls, session, merchant_id, is_online, commit=True):
        session.query(CooperateRoomTypeModel)\
                .filter(CooperateRoomTypeModel.merchant_id == merchant_id)\
                .update({CooperateRoomTypeModel.is_online: is_online})
        if commit:
            session.commit()


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
                is_delete = self.is_delete,
                )

