# -*- coding: utf-8 -*-

from __future__ import absolute_import

import datetime

from tornado.util import ObjectDict

from models import Base
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
    day1 = Column(VARCHAR(50), nullable=False, default="-1|-1")
    day2 = Column(VARCHAR(50), nullable=False, default="-1|-1")
    day3 = Column(VARCHAR(50), nullable=False, default="-1|-1")
    day4 = Column(VARCHAR(50), nullable=False, default="-1|-1")
    day5 = Column(VARCHAR(50), nullable=False, default="-1|-1")
    day6 = Column(VARCHAR(50), nullable=False, default="-1|-1")
    day7 = Column(VARCHAR(50), nullable=False, default="-1|-1")
    day8 = Column(VARCHAR(50), nullable=False, default="-1|-1")
    day9 = Column(VARCHAR(50), nullable=False, default="-1|-1")
    day10 = Column(VARCHAR(50), nullable=False, default="-1|-1")
    day11 = Column(VARCHAR(50), nullable=False, default="-1|-1")
    day12 = Column(VARCHAR(50), nullable=False, default="-1|-1")
    day13 = Column(VARCHAR(50), nullable=False, default="-1|-1")
    day14 = Column(VARCHAR(50), nullable=False, default="-1|-1")
    day15 = Column(VARCHAR(50), nullable=False, default="-1|-1")
    day16 = Column(VARCHAR(50), nullable=False, default="-1|-1")
    day17 = Column(VARCHAR(50), nullable=False, default="-1|-1")
    day18 = Column(VARCHAR(50), nullable=False, default="-1|-1")
    day19 = Column(VARCHAR(50), nullable=False, default="-1|-1")
    day20 = Column(VARCHAR(50), nullable=False, default="-1|-1")
    day21 = Column(VARCHAR(50), nullable=False, default="-1|-1")
    day22 = Column(VARCHAR(50), nullable=False, default="-1|-1")
    day23 = Column(VARCHAR(50), nullable=False, default="-1|-1")
    day24 = Column(VARCHAR(50), nullable=False, default="-1|-1")
    day25 = Column(VARCHAR(50), nullable=False, default="-1|-1")
    day26 = Column(VARCHAR(50), nullable=False, default="-1|-1")
    day27 = Column(VARCHAR(50), nullable=False, default="-1|-1")
    day28 = Column(VARCHAR(50), nullable=False, default="-1|-1")
    day29 = Column(VARCHAR(50), nullable=False, default="-1|-1")
    day30 = Column(VARCHAR(50), nullable=False, default="-1|-1")
    day31 = Column(VARCHAR(50), nullable=False, default="-1|-1")
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
    def get_by_roomtype_id_and_date(cls, session, roomtype_id, year, month):
        month = InventoryModel.combin_year_month(year, month)
        return session.query(InventoryModel)\
                .filter(InventoryModel.roomtype_id == roomtype_id)\
                .filter(InventoryModel.month == month)\
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
        '''
        days as [(year, months),]
        '''
        months = [InventoryModel.combin_year_month(day[0], day[1]) for day in days]
        return session.query(InventoryModel)\
                .filter(InventoryModel.merchant_id == merchant_id)\
                .filter(InventoryModel.hotel_id == hotel_id)\
                .filter(InventoryModel.roomtype_id == roomtype_id)\
                .filter(InventoryModel.month.in_(months))\
                .filter(InventoryModel.is_delete == 0)\
                .all()

    @classmethod
    def get_by_merchant_and_dates(cls, session, merchant_id, days):
        '''
        days as [(year, months),]
        '''
        months = [InventoryModel.combin_year_month(day[0], day[1]) for day in days]
        return session.query(InventoryModel)\
                .filter(InventoryModel.merchant_id == merchant_id)\
                .filter(InventoryModel.month.in_(months))\
                .filter(InventoryModel.is_delete == 0)\
                .all()

    @classmethod
    def get_by_roomtype_and_dates(cls, session, roomtype_id, days):
        '''
        days as [(year, months),]
        '''
        months = [InventoryModel.combin_year_month(day[0], day[1]) for day in days]
        return session.query(InventoryModel)\
                .filter(InventoryModel.roomtype_id == roomtype_id)\
                .filter(InventoryModel.month.in_(months))\
                .filter(InventoryModel.is_delete == 0)\
                .all()

    @classmethod
    def delete_by_roomtype_id(cls, session, roomtype_id, commit=True):
        session.query(InventoryModel)\
                .filter(InventoryModel.roomtype_id == roomtype_id)\
                .filter(InventoryModel.is_delete == 0)\
                .update({'isDelete': 1})
        if commit:
            session.commit()
        else:
            session.flush()


    @classmethod
    def insert_by_year(cls, session, merchant_id, hotel_id, roomtype_id, base_hotel_id, base_roomtype_id, year):
        inventories = []
        for month in range(1,13):
            inventory = cls.get_by_merchant_hotel_roomtype_date(session, merchant_id, hotel_id, roomtype_id, year, month)
            if inventory:
                continue
            else:
                _month = InventoryModel.combin_year_month(year, month)
                inventory = InventoryModel(merchant_id=merchant_id, hotel_id=hotel_id, roomtype_id=roomtype_id, base_hotel_id=base_hotel_id, base_roomtype_id=base_roomtype_id, month=_month)
                inventories.append(inventory)

        session.add_all(inventories)
        session.commit()
        return inventories

    @classmethod
    def insert_in_months(cls, session, merchant_id, hotel_id, roomtype_id, base_hotel_id, base_roomtype_id, months, commit=True):
        inventories = []
        dates= cls.get_months(months)
        for date in dates:
            inventory = cls.get_by_merchant_hotel_roomtype_date(session, merchant_id, hotel_id, roomtype_id, date[0], date[1])
            if inventory:
                continue
            else:
                _month = InventoryModel.combin_year_month(date[0], date[1])
                inventory = InventoryModel(merchant_id=merchant_id, hotel_id=hotel_id, roomtype_id=roomtype_id, month=_month, base_hotel_id=base_hotel_id, base_roomtype_id=base_roomtype_id)
                inventories.append(inventory)
        session.add_all(inventories)
        if commit:
            session.commit()
        else:
            session.flush()
        return inventories

    @classmethod
    def insert_in_four_month(cls, session, merchant_id, hotel_id, roomtype_id, base_hotel_id, base_roomtype_id):
        inventories = []
        dates= cls.get_months(4)
        for date in dates:
            inventory = cls.get_by_merchant_hotel_roomtype_date(session, merchant_id, hotel_id, roomtype_id, date[0], date[1])
            if inventory:
                continue
            else:
                _month = InventoryModel.combin_year_month(date[0], date[1])
                inventory = InventoryModel(merchant_id=merchant_id, hotel_id=hotel_id, roomtype_id=roomtype_id, month=_month, base_hotel_id=base_hotel_id, base_roomtype_id=base_roomtype_id)
                inventories.append(inventory)
        session.add_all(inventories)
        session.commit()
        return inventories

    @classmethod
    def insert_all_in_months(cls, session, roomtypes, months):

        inventories = []
        dates= cls.get_months(months)

        for roomtype in roomtypes:
            for date in dates:
                inventory = cls.get_by_roomtype_id_and_date(session, roomtype.id, date[0], date[1])
                if inventory:
                    continue
                else:
                    _month = InventoryModel.combin_year_month(date[0], date[1])
                    inventory = InventoryModel(merchant_id=roomtype.merchant_id, hotel_id=roomtype.hotel_id, roomtype_id=roomtype.id, month=_month, base_hotel_id=roomtype.base_hotel_id, base_roomtype_id=roomtype.base_roomtype_id)
                    inventories.append(inventory)
        session.add_all(inventories)
        session.commit()
        return inventories

    @classmethod
    def insert_all_in_four_month(cls, session, roomtypes):

        inventories = []
        dates= cls.get_months(4)

        for roomtype in roomtypes:
            for date in dates:
                inventory = cls.get_by_roomtype_id_and_date(session, roomtype.id, date[0], date[1])
                if inventory:
                    continue
                else:
                    _month = InventoryModel.combin_year_month(date[0], date[1])
                    inventory = InventoryModel(merchant_id=roomtype.merchant_id, hotel_id=roomtype.hotel_id, roomtype_id=roomtype.id, month=_month, base_hotel_id=roomtype.base_hotel_id, base_roomtype_id=roomtype.base_roomtype_id)
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

        for i in range(n):
            if month > 12:
                month = month - 12
                year = year + 1
            dates.append((year, month))
            month = month + 1

        return dates

    @classmethod
    def update(cls, session, merchant_id, hotel_id, roomtype_id, year, month, day, price_type, val):
        inventory = cls.get_by_merchant_id_and_hotel_id_and_date(session, merchant_id, hotel_id, roomtype_id, year, month)
        val = val if val >= 0 else 0
        val = val if val <= 99 else 99
        if not inventory:
            return
        inventory.set_val_by_day(day, price_type, val)
        session.commit()



    @classmethod
    def combin_year_month(cls, year, month):
        return int("{}{:0>2d}".format(year, month))


    def get_day(self, day, type=None):
        if day < 1 or day > 31:
            return 0
        day_key = 'day' + str(day)
        value = getattr(self, day_key)
        if type:
            return int(value.split('|')[type])
        else:
            prices = value.split('|')
            auto, manual = int(prices[0]), int(prices[1])
            auto = auto if auto >=0 else 0
            manual = manual if manual >= 0 else 0
            return auto + manual

    def get_day_count(self, day):
        if day < 1 or day > 31:
            return 0
        day_key = 'day' + str(day)
        value = getattr(self, day_key)
        counts = value.split('|')
        return int(counts[0]), int(counts[1])

    def deduct_val_by_day(self, day, val):
        day_key = 'day' + str(day)
        value = getattr(self, day_key)
        count_auto, count_manual = [count if count >= 0 else 0 for count in [int(count) for count in value.split('|')]]

        if count_auto + count_manual < val:
            return -1, -1

        if count_auto >= val:
            num_auto = val
            num_manual = 0
            remain_auto = count_auto - num_auto
            remain_manual = count_manual
        else:
            num_auto = count_auto
            num_manual = val - num_auto
            remain_auto = 0
            remain_manual = count_manual - num_manual

        value = "{}|{}".format(remain_auto, remain_manual)
        setattr(self, day_key, value)

        return num_auto, num_manual

    def recovery_val_by_day(self, day, num_auto, num_manual):
        day_key = 'day' + str(day)
        value = getattr(self, day_key)
        count_auto, count_manual = [count if count >= 0 else 0 for count in [int(count) for count in value.split('|')]]

        value = "{}|{}".format(count_auto + num_auto, count_manual + num_manual)
        setattr(self, day_key, value)

        return num_auto, num_manual

    def add_val_by_day(self, day, price_type, val):
        day_key = 'day' + str(day)
        value = getattr(self, day_key)
        count_auto, count_manual = [int(count) for count in value.split('|')]
        if price_type == 0:
            remain_manual = count_manual
            remain_auto = count_auto if count_auto >= 0 else 0
            remain_auto = remain_auto + val
            remain_auto = self.fix_inventory_count_range(remain_auto)
        else:
            remain_auto = count_auto
            remain_manual = count_manual if count_manual >= 0 else 0
            remain_manual = remain_manual + val
            remain_manual = self.fix_inventory_count_range(remain_manual)

        value = "{}|{}".format(remain_auto, remain_manual)
        setattr(self, day_key, value)

    def fix_inventory_count_range(self, count):
        count = count if count >= 0 else 0
        count = count if count <= 99 else 99
        return count

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



