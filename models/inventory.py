# -*- coding: utf-8 -*-

import datetime

from tornado.util import ObjectDict

from tasks.models import Base
from sqlalchemy import Column
from sqlalchemy.dialects.mysql import BIT, INTEGER, VARCHAR, DATETIME, BIGINT

class InventoryModel(Base):

    __tablename__ = 'inventory'
    __table_args__ = {
        'mysql_charset': 'utf8', 'mysql_engine': 'InnoDB'}

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    merchant_id = Column("merchantId", INTEGER, nullable=False, default=0)
    hotel_id = Column("hotelId", INTEGER, nullable=False, default=0)
    roomtype_id = Column("roomTypeId", INTEGER, nullable=False, default=0)
    base_hotel_id = Column("baseHotelId", INTEGER, nullable=False, default=0)
    base_roomtype_id = Column("baseRoomTypeId", INTEGER, nullable=False, default=0)
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

    @classmethod
    def get_by_id(cls, session, id):
        return session.query(InventoryModel)\
                .filter(InventoryModel.id == id)\
                .filter(InventoryModel.is_delete == 0)\
                .first()

    @classmethod
    def get_by_merchant_id_and_hotel_id(cls, session, merchant_id, hotel_id):
        return session.query(InventoryModel)\
                .filter(InventoryModel.merchant_id == merchant_id)\
                .filter(InventoryModel.hotel_id == hotel_id)\
                .filter(InventoryModel.is_delete == 0)\
                .all()


    @classmethod
    def get_by_merchant_id_and_hotel_id_and_date(cls, session, merchant_id, hotel_id, year, month):
        month = InventoryModel.combin_year_month(year, month)
        return session.query(InventoryModel)\
                .filter(InventoryModel.merchant_id == merchant_id)\
                .filter(InventoryModel.hotel_id == hotel_id)\
                .filter(InventoryModel.month == month)\
                .filter(InventoryModel.is_delete == 0)\
                .all()

    @classmethod
    def get_by_merchant_id_and_hotel_id_and_days(cls, session, merchant_id, hotel_id, days):
        months = [InventoryModel.combin_year_month(day[0], day[1]) for day in days]
        return session.query(InventoryModel)\
                .filter(InventoryModel.merchant_id == merchant_id)\
                .filter(InventoryModel.hotel_id == hotel_id)\
                .filter(InventoryModel.month.in_(months))\
                .filter(InventoryModel.is_delete == 0)\
                .all()

    @classmethod
    def get_by_merchant_hotel_roomtype_date(cls, session, merchant_id, hotel_id, roomtype_id, year, month):
        month = InventoryModel.combin_year_month(year, month)
        return session.query(InventoryModel)\
                .filter(InventoryModel.merchant_id == merchant_id)\
                .filter(InventoryModel.hotel_id == hotel_id)\
                .filter(InventoryModel.roomtype_id == roomtype_id)\
                .filter(InventoryModel.month == month)\
                .filter(InventoryModel.is_delete == 0)\
                .all()
    @classmethod
    def get_by_merchant_hotel_roomtype_dates(cls, session, merchant_id, hotel_id, roomtype_id, days):
        months = [InventoryModel.combin_year_month(day[0], day[1]) for day in days]
        return session.query(InventoryModel)\
                .filter(InventoryModel.merchant_id == merchant_id)\
                .filter(InventoryModel.hotel_id == hotel_id)\
                .filter(InventoryModel.roomtype_id == roomtype_id)\
                .filter(InventoryModel.month.in_(months))\
                .filter(InventoryModel.is_delete == 0)\
                .all()

    @classmethod
    def insert_by_year(cls, session, merchant_id, hotel_id, roomtype_id, year):
        for month in range(1,13):
            inventory = cls.get_by_merchant_hotel_roomtype_date(session, merchant_id, hotel_id, roomtype_id, year, month)
            if inventory:
                continue
            else:
                _month = InventoryModel.combin_year_month(year, month)
                inventory = InventoryModel(merchant_id=merchant_id, hotel_id=hotel_id, roomtype_id=roomtype_id, month=_month)
                session.add(inventory)
        session.commit()

    @classmethod
    def insert_in_four_month(cls, session, merchant_id, cooperate_hotel_id, hotel_id, roomtype_id):
        inventories = []
        dates= cls.get_months(4)
        for date in dates:
            inventory = cls.get_by_merchant_hotel_roomtype_date(session, merchant_id, hotel_id, roomtype_id, date[0], date[1])
            if inventory:
                continue
            else:
                _month = InventoryModel.combin_year_month(date[0], date[1])
                inventory = InventoryModel(merchant_id=merchant_id, hotel_id=hotel_id, roomtype_id=roomtype_id, month=_month, cooperate_hotel_id=cooperate_hotel_id)
                inventories.append(inventory)
        session.add_all(inventories)
        session.commit()
        return inventories


    @classmethod
    def get_by_room_ids_and_months(cls, session, roomtype_ids, months):
        return session.query(InventoryModel)\
                .filter(InventoryModel.roomtype_id.in_(roomtype_ids))\
                .filter(InventoryModel.month.in_(months))\
                .filter(InventoryModel.is_delete == 0)\
                .all()

    @classmethod
    def complete_in_four_months(cls, session, roomtype_ids):
        dates = cls.get_months(4)
        months = [cls.combin_year_month(date[0], date[1]) for date in dates]
        inventories = cls.get_by_room_ids_and_months(session, roomtype_ids, months)
        need_complete_roomtype_ids = []
        for roomtype_id in roomtype_ids:
            for month in months:
                for inventory in inventories:
                    if inventory.roomtype_id == roomtype_id and inventory.month == month:
                        break
                else:
                    need_complete_roomtype_ids.append(roomtype_id)




    @classmethod
    def get_months(cls, n):
        today = datetime.date.today()
        year, month = today.year, today.month

        dates = []

        _year = year
        for i in range(n):
            _month = month + i
            if _month > 12:
                _month = _month - 12
                _year = _year + 1
            dates.append((_year, _month))

        return dates




    @classmethod
    def update(cls, session, merchant_id, hotel_id, roomtype_id, year, month, day, price_type, val):
        inventory = cls.get_by_merchant_id_and_hotel_id_and_date(session, merchant_id, hotel_id, roomtype_id, year, month)
        if not inventory:
            return
        _val = inventory.get_day(day, price_type)
        if _val + val < 0:
            return

        inventory.set_val_by_day(day, price_type, val)
        session.commit()



    @classmethod
    def combin_year_month(cls, year, month):
        return int("{}{:0>2d}".format(year, month))


    def get_day(self, day, type=0):
        if day < 1 or day > 31:
            return 0
        day_key = 'day' + str(day)
        value = getattr(self, day_key)
        return int(value.split('|')[type])

    def add_val_by_day(self, day, price_type, val):
        day_key = 'day' + str(day)
        value = getattr(self, day_key)
        price_reserved, price_manual = value.split('|')
        if price_type == 0:
            price_reserved = int(price_reserved) + val
            price_reserved = price_reserved if price_reserved >= 0 else 0
        else:
            price_manual = int(price_manual) + val
            price_manual = price_manual if price_manual >= 0 else 0

        value = "{}|{}".format(price_reserved, price_manual)
        setattr(self, day_key, value)

    def set_val_by_day(self, day, price_type, val):
        day_key = 'day' + str(day)
        value = getattr(self, day_key)
        price_reserved, price_manual = value.split('|')
        if price_type == 0:
            price_reserved = val
        else:
            price_manual = val

        value = "{}|{}".format(price_reserved, price_manual)
        setattr(self, day_key, value)

    def todict(self):
        return ObjectDict(
                id=self.id,
                merchant_id=self.merchant_id,
                hotel_id=self.hotel_id,
                roomtype_id=self.roomtype_id,
                base_hotel_id=self.base_hotel_id,
                base_roomtype_id=self.base_roomtype_id,
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



