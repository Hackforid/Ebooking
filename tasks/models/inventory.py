# -*- coding: utf-8 -*-

from tornado.util import ObjectDict

from tasks.models import Base
from sqlalchemy import Column
from sqlalchemy.dialects.mysql import BIT, INTEGER, VARCHAR, DATETIME, BIGINT

from tasks.celery_app import app
from tasks.base_task import SqlAlchemyTask


class InventoryModel(Base):

    __tablename__ = 'inventory'
    __table_args__ = {
        'mysql_charset': 'utf8', 'mysql_engine': 'InnoDB'}

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    merchant_id = Column("merchantId", INTEGER, nullable=False, default=0)
    hotel_id = Column("hotelId", INTEGER, nullable=False, default=0)
    roomtype_id = Column("roomTypeId", INTEGER, nullable=False, default=0)
    month = Column(INTEGER, nullable=False, default=0)
    day1 = Column(VARCHAR(50), nullable=False, default="0|0")
    day2 = Column(VARCHAR(50), nullable=False, default="0|0")
    day3 = Column(VARCHAR(50), nullable=False, default="0|0")
    day4 = Column(VARCHAR(50), nullable=False, default="0|0")
    day5 = Column(VARCHAR(50), nullable=False, default="0|0")
    day6 = Column(VARCHAR(50), nullable=False, default="0|0")
    day7 = Column(VARCHAR(50), nullable=False, default="0|0")
    day8 = Column(VARCHAR(50), nullable=False, default="0|0")
    day9 = Column(VARCHAR(50), nullable=False, default="0|0")
    day10 = Column(VARCHAR(50), nullable=False, default="0|0")
    day11 = Column(VARCHAR(50), nullable=False, default="0|0")
    day12 = Column(VARCHAR(50), nullable=False, default="0|0")
    day13 = Column(VARCHAR(50), nullable=False, default="0|0")
    day14 = Column(VARCHAR(50), nullable=False, default="0|0")
    day15 = Column(VARCHAR(50), nullable=False, default="0|0")
    day16 = Column(VARCHAR(50), nullable=False, default="0|0")
    day17 = Column(VARCHAR(50), nullable=False, default="0|0")
    day18 = Column(VARCHAR(50), nullable=False, default="0|0")
    day19 = Column(VARCHAR(50), nullable=False, default="0|0")
    day20 = Column(VARCHAR(50), nullable=False, default="0|0")
    day21 = Column(VARCHAR(50), nullable=False, default="0|0")
    day22 = Column(VARCHAR(50), nullable=False, default="0|0")
    day23 = Column(VARCHAR(50), nullable=False, default="0|0")
    day24 = Column(VARCHAR(50), nullable=False, default="0|0")
    day25 = Column(VARCHAR(50), nullable=False, default="0|0")
    day26 = Column(VARCHAR(50), nullable=False, default="0|0")
    day27 = Column(VARCHAR(50), nullable=False, default="0|0")
    day28 = Column(VARCHAR(50), nullable=False, default="0|0")
    day29 = Column(VARCHAR(50), nullable=False, default="0|0")
    day30 = Column(VARCHAR(50), nullable=False, default="0|0")
    day31 = Column(VARCHAR(50), nullable=False, default="0|0")
    is_online = Column('isOnline', BIT, nullable=False, default=0)
    is_delete = Column('isDelete', BIT, nullable=False, default=0)

    @staticmethod
    @app.task(base=SqlAlchemyTask, bind=True)
    def get_by_id(task_self, id):
        return task_self.session.query(InventoryModel)\
                .filter(InventoryModel.id == id)\
                .filter(InventoryModel.is_delete == 0)\
                .first()

    @staticmethod
    @app.task(base=SqlAlchemyTask, bind=True)
    def get_by_merchant_id_and_hotel_id(task_self, merchant_id, hotel_id):
        return task_self.session.query(InventoryModel)\
                .filter(InventoryModel.merchant_id == merchant_id)\
                .filter(InventoryModel.hotel_id == hotel_id)\
                .filter(InventoryModel.is_delete == 0)\
                .all()


    @staticmethod
    @app.task(base=SqlAlchemyTask, bind=True)
    def get_by_merchant_id_and_hotel_id_and_date(task_self, merchant_id, hotel_id, year, month):
        month = InventoryModel.combin_year_month(year, month)
        return task_self.session.query(InventoryModel)\
                .filter(InventoryModel.merchant_id == merchant_id)\
                .filter(InventoryModel.hotel_id == hotel_id)\
                .filter(InventoryModel.month == month)\
                .filter(InventoryModel.is_delete == 0)\
                .all()

    @staticmethod
    @app.task(base=SqlAlchemyTask, bind=True)
    def get_by_merchant_hotel_roomtype_date(task_self, merchant_id, hotel_id, roomtype_id, year, month):
        month = InventoryModel.combin_year_month(year, month)
        return task_self.session.query(InventoryModel)\
                .filter(InventoryModel.merchant_id == merchant_id)\
                .filter(InventoryModel.hotel_id == hotel_id)\
                .filter(InventoryModel.roomtype_id == roomtype_id)\
                .filter(InventoryModel.month == month)\
                .filter(InventoryModel.is_delete == 0)\
                .all()

    @staticmethod
    @app.task(base=SqlAlchemyTask, bind=True)
    def insert_by_year(task_self, merchant_id, hotel_id, roomtype_id, year):
        for month in range(1,13):
            inventory = InventoryModel.get_by_merchant_hotel_roomtype_date(merchant_id, hotel_id, roomtype_id, year, month)
            if inventory:
                continue
            else:
                _month = InventoryModel.combin_year_month(year, month)
                inventory = InventoryModel(merchant_id=merchant_id, hotel_id=hotel_id, roomtype_id=roomtype_id, month=_month)
                task_self.session.add(inventory)
        task_self.session.commit()

    @staticmethod
    def combin_year_month(year, month):
        return int("{}{:0>2d}".format(year, month))

    def todict(self):
        return ObjectDict(
                id=self.id,
                merchant_id=self.merchant_id,
                hotel_id=self.hotel_id,
                roomtype_id=self.roomtype_id,
                month=self.month,
                day1=self.day1,
                day2=self.day2,
                day3=self.day3,
                day4=self.day4,
                day5=self.day5,
                day6=self.day6,
                day7=self.day7,
                day8=self.day8,
                day9=self.day9,
                day10=self.day10,
                day11=self.day11,
                day12=self.day12,
                day13=self.day13,
                day14=self.day14,
                day15=self.day15,
                day16=self.day16,
                day17=self.day17,
                day18=self.day18,
                day19=self.day19,
                day20=self.day20,
                day21=self.day21,
                day22=self.day22,
                day23=self.day23,
                day24=self.day24,
                day25=self.day25,
                day26=self.day26,
                day27=self.day27,
                day28=self.day28,
                day29=self.day29,
                day30=self.day30,
                day31=self.day31,
                is_online=self.is_online,
                is_delete=self.is_delete,
                )



