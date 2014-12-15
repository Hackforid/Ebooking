# -*- coding: utf-8 -*-

import datetime

from tornado.util import ObjectDict 

from tasks.models import Base
from sqlalchemy import Column
from sqlalchemy.dialects.mysql import BIT, INTEGER, VARCHAR, DATETIME, BIGINT

from tasks.celery_app import app
from tasks.base_task import SqlAlchemyTask


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

    @staticmethod
    @app.task(base=SqlAlchemyTask, bind=True)
    def get_by_merchant_id_and_hotel_id(task_self, merchant_id, hotel_id):
        return task_self.session.query(CooperateRoomTypeModel)\
                .filter(CooperateRoomTypeModel.merchant_id == merchant_id)\
                .filter(CooperateRoomTypeModel.hotel_id == hotel_id)\
                .filter(CooperateRoomTypeModel.is_delete == 0)\
                .all()


    @staticmethod
    @app.task(base=SqlAlchemyTask, bind=True)
    def new_roomtype_coops(task_self, merchant_id, hotel_id, roomtype_ids):
        coops = []
        try:

            for roomtype_id in roomtype_ids:
                coop = CooperateRoomTypeModel(merchant_id=merchant_id, hotel_id=hotel_id, roomtype_id=roomtype_id)
                coops.append(coop)

            task_self.session.add_all(coops)
            task_self.session.commit()

            for coop in coops:
                print coop.todict()
        except:
            task_self.session.rollback()
            return

        from tasks.models.inventory import InventoryModel
        toyear = datetime.date.today().year
        for roomtype_id in roomtype_ids:
            InventoryModel.insert_by_year(merchant_id, hotel_id, roomtype_id, toyear)

        return coops

    def todict(self):
        return ObjectDict(
                id = self.id,
                merchant_id = self.merchant_id,
                hotel_id = self.hotel_id,
                roomtype_id = self.roomtype_id,
                is_online = self.is_online,
                )

