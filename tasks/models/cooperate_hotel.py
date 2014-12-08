# -*- coding: utf-8 -*-

from tornado.util import ObjectDict 

from models import Base
from sqlalchemy import Column
from sqlalchemy.dialects.mysql import BIT, INTEGER, VARCHAR, DATETIME, BIGINT

from tasks.celery_app import app
from tasks.base_task import SqlAlchemyTask


class CooperateHotelModel(Base):

    __tablename__ = 'cooperateHotel'
    __table_args__ = {
        'mysql_charset': 'utf8', 'mysql_engine': 'InnoDB'}

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    merchant_id = Column("merchantId", INTEGER, nullable=False, default=0)
    hotel_id = Column("hotelId", INTEGER, nullable=False, default=0)
    is_online = Column('isOnline', BIT, nullable=False, default=0)
    is_delete = Column('isDelete', BIT, nullable=False, default=0)

    @staticmethod
    @app.task(base=SqlAlchemyTask, bind=True)
    def get_by_id(task_self, id):
        return task_self.session.query(CooperateHotelModel)\
                .filter(CooperateHotelModel.id == id)\
                .filter(CooperateHotelModel.is_delete == 0)\
                .first()

    @staticmethod
    @app.task(base=SqlAlchemyTask, bind=True)
    def get_by_merchant_id(task_self, merchant_id):
        return task_self.session.query(CooperateHotelModel)\
                .filter(CooperateHotelModel.merchant_id == merchant_id)\
                .filter(CooperateHotelModel.is_delete == 0)\
                .all()

    @staticmethod
    @app.task(base=SqlAlchemyTask, bind=True)
    def get_by_merchant_id_and_hotel_id(task_self, merchant_id, hotel_id):
        return task_self.session.query(CooperateHotelModel)\
                .filter(CooperateHotelModel.merchant_id == merchant_id)\
                .filter(CooperateHotelModel.hotel_id == hotel_id)\
                .filter(CooperateHotelModel.is_delete == 0)\
                .first()

    @staticmethod
    @app.task(base=SqlAlchemyTask, bind=True)
    def new_hotel_cooprate(task_self, merchant_id, hotel_id):
        coop = CooperateHotelModel(merchant_id=merchant_id, hotel_id=hotel_id)
        task_self.session.add(coop)
        task_self.session.commit()

        print 'new coop', coop.id

        return coop

    @staticmethod
    @app.task(base=SqlAlchemyTask, bind=True)
    def delete_hotel_cooprate(task_self, merchant_id, hotel_id):
        coop = CooperateHotelModel.get_by_merchant_id_and_hotel_id(task_self, merchant_id, hotel_id)
        if coop:
            coop.is_delete = 1
            task_self.session.commit()
        return coop

    def todict(self):
        return ObjectDict(
                id=self.id,
                merchant_id=self.merchant_id,
                hotel_id=self.hotel_id,
                is_online=self.is_online,
                )

