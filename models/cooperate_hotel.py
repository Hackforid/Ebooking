# -*- coding: utf-8 -*-

from tornado.util import ObjectDict

from sqlalchemy import Column
from sqlalchemy.dialects.mysql import BIT, INTEGER, VARCHAR, DATETIME, BIGINT


from models import Base

class CooperateHotelModel(Base):

    __tablename__ = 'cooperateHotel'
    __table_args__ = {
        'mysql_charset': 'utf8', 'mysql_engine': 'InnoDB'}

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    merchant_id = Column("merchantId", INTEGER, nullable=False, default=0)
    base_hotel_id = Column("baseHotelId", INTEGER, nullable=False, default=0)
    is_online = Column('isOnline', BIT, nullable=False, default=1)
    is_delete = Column('isDelete', BIT, nullable=False, default=0)

    @classmethod
    def get_by_id(cls, session, id):
        return session.query(CooperateHotelModel)\
            .filter(CooperateHotelModel.id == id)\
            .filter(CooperateHotelModel.is_delete == 0)\
            .first()

    @classmethod
    def get_by_merchant_id(cls, session, merchant_id):
        return session.query(CooperateHotelModel)\
            .filter(CooperateHotelModel.merchant_id == merchant_id)\
            .filter(CooperateHotelModel.is_delete == 0)\
            .all()

    @classmethod
    def get_by_merchant_id_and_hotel_id(cls, session, merchant_id, hotel_id):
        return session.query(CooperateHotelModel)\
            .filter(CooperateHotelModel.id == hotel_id)\
            .filter(CooperateHotelModel.merchant_id == merchant_id)\
            .filter(CooperateHotelModel.is_delete == 0)\
            .first()

    @classmethod
    def get_by_merchant_id_and_base_hotel_id(cls, session, merchant_id, base_hotel_id):
        return session.query(CooperateHotelModel)\
            .filter(CooperateHotelModel.merchant_id == merchant_id)\
            .filter(CooperateHotelModel.base_hotel_id == base_hotel_id)\
            .filter(CooperateHotelModel.is_delete == 0)\
            .first()

    @classmethod
    def new_hotel_cooprate(cls, session, merchant_id, base_hotel_id):
        coop = CooperateHotelModel(merchant_id=merchant_id, base_hotel_id=base_hotel_id)
        session.add(coop)
        session.commit()

        return coop

    @classmethod
    def new_hotel_cooprates(cls, session, merchant_id, base_hotel_ids):
        coops = []
        for base_hotel_id in base_hotel_ids:
            coop = cls.get_by_merchant_id_and_base_hotel_id(session, merchant_id, base_hotel_id)
            if not coop:
                coop = CooperateHotelModel(merchant_id=merchant_id, base_hotel_id=base_hotel_id)
            coops.append(coop)
        session.add_all(coops)
        session.commit()

        return coops

    @classmethod
    def delete_hotel_cooprate(cls, session, merchant_id, base_hotel_id):
        coop = cls.get_by_merchant_id_and_hotel_id(
            session, merchant_id, base_hotel_id)
        if coop:
            coop.is_delete = 1
            session.commit()
        return coop

    def todict(self):
        return ObjectDict(
            id=self.id,
            merchant_id=self.merchant_id,
            base_hotel_id=self.base_hotel_id,
            is_online=self.is_online,
        )
