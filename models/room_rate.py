# -*- coding: utf-8 -*-

from datetime import datetime, timedelta

from tornado.util import ObjectDict

from tasks.models import Base
from sqlalchemy import Column
from sqlalchemy.dialects.mysql import BIT, INTEGER, VARCHAR, DATE, TIME, TIMESTAMP, BIGINT, TINYINT


class RoomRateModel(Base):

    __tablename__ = 'roomRate'
    __table_args__ = {
        'mysql_charset': 'utf8', 'mysql_engine': 'InnoDB'}

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    hotel_id = Column("hotelId", INTEGER, nullable=False, default=0)
    roomtype_id = Column("roomTypeId", INTEGER, nullable=False, default=0)
    rate_plan_id = Column("ratePlanId", INTEGER, nullable=False, default=0)
    month1 = Column(VARCHAR(500), nullable=False,
                    default='-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1')
    month2 = Column(VARCHAR(500), nullable=False,
                    default='-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1')
    month3 = Column(VARCHAR(500), nullable=False,
                    default='-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1')
    month4 = Column(VARCHAR(500), nullable=False,
                    default='-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1')
    month5 = Column(VARCHAR(500), nullable=False,
                    default='-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1')
    month6 = Column(VARCHAR(500), nullable=False,
                    default='-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1')
    month7 = Column(VARCHAR(500), nullable=False,
                    default='-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1')
    month8 = Column(VARCHAR(500), nullable=False,
                    default='-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1')
    month9 = Column(VARCHAR(500), nullable=False,
                    default='-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1')
    month10 = Column(VARCHAR(500), nullable=False,
                     default='-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1')
    month11 = Column(VARCHAR(500), nullable=False,
                     default='-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1')
    month12 = Column(VARCHAR(500), nullable=False,
                     default='-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1')
    meal1 = Column(VARCHAR(150), nullable=False,
                   default='-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1')
    meal2 = Column(VARCHAR(150), nullable=False,
                   default='-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1')
    meal3 = Column(VARCHAR(150), nullable=False,
                   default='-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1')
    meal4 = Column(VARCHAR(150), nullable=False,
                   default='-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1')
    meal5 = Column(VARCHAR(150), nullable=False,
                   default='-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1')
    meal6 = Column(VARCHAR(150), nullable=False,
                   default='-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1')
    meal7 = Column(VARCHAR(150), nullable=False,
                   default='-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1')
    meal8 = Column(VARCHAR(150), nullable=False,
                   default='-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1')
    meal9 = Column(VARCHAR(150), nullable=False,
                   default='-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1')
    meal10 = Column(VARCHAR(150), nullable=False,
                    default='-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1')
    meal11 = Column(VARCHAR(150), nullable=False,
                    default='-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1')
    meal12 = Column(VARCHAR(150), nullable=False,
                    default='-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1')
    is_online = Column('isOnline', BIT, nullable=False, default=0)
    is_delete = Column('isDelete', BIT, nullable=False, default=0)
    ts_update = Column("tsUpdate", TIMESTAMP)

    @classmethod
    def get_by_id(cls, session, id):
        return session.query(RoomRateModel)\
                .filter(RoomRateModel.id == id)\
                .filter(RoomRateModel.is_delete == 0)\
                .first()

    @classmethod
    def get_by_rateplan(cls, session, rate_plan_id):
        return session.query(RoomRateModel)\
                .filter(RoomRateModel.rate_plan_id == rate_plan_id)\
                .filter(RoomRateModel.is_delete == 0)\
                .first()

    @classmethod
    def new_roomrate(cls, session, hotel_id, roomtype_id, rate_plan_id, commit=True):
        room = RoomRateModel(hotel_id=hotel_id,
                             roomtype_id=roomtype_id, rate_plan_id=rate_plan_id)
        session.add(room)
        if commit:
            session.commit()

        return room

    @classmethod
    def set_meal(cls, session, rate_plan_id, meal_num, commit=True):
        room = cls.get_by_rateplan(session, rate_plan_id)
        meal_num = str(meal_num)
        meal = str('|'.join([meal_num for i in range(0, 31)]))
        for i in range(1, 13):
            key = 'meal{}'.format(i)
            setattr(room, key, meal)
        if commit:
            session.commit()
        return room

    @classmethod
    def set_price(cls, session, id, price, start_date, end_date):
        roomrate = cls.get_by_id(session, id)


        year0, year1 = start_date.year, end_date.year
        if year0 == year1:
            roomrate.change_price_in_ayear(price, start_date, end_date)
        else:
            roomrate.change_price_in_ayear(price, start_date, datetime(year0, 12, 31))
            roomrate.change_price_in_ayear(price, datetime(year1, 1, 1), end_date)

        session.commit()
        return roomrate

    def change_price_in_ayear(self, price, start_date, end_date):
        month0, month1 = start_date.month, end_date.month
        if month0 == month1:
            day0, day1 = start_date.day, end_date.day
            self.change_price(price, month0, start_date, end_date)
        else:
            for month in range(month0, month1 + 1):
                if month == month0:
                    self.change_price(price, month, start_date.day, 31)
                elif month == month1:
                    self.change_price(price, month, 1, end_date.day)
                else:
                    self.change_price(price, month, 1, 31)




    def change_price(self, price, month, start_day, end_day):
        month_key = 'month{}'.format(month)
        prices = getattr(self, month_key)
        setattr(self, month_key, self.get_updated_price(prices, price, start_day, end_day))


    def get_updated_price(self, prices, price, start, end):
        prices = prices.split('|')
        price = str(price)
        for i in range(start.day, end.day+1):
            prices[i-1] = price

        return '|'.join(prices)



    def todict(self):
        return ObjectDict(
                id=self.id,
                hotel_id=self.hotel_id,
                roomtype_id=self.roomtype_id,
                rate_plan_id=self.rate_plan_id,
                month1=self.month1,
                month2=self.month2,
                month3=self.month3,
                month4=self.month4,
                month5=self.month5,
                month6=self.month6,
                month7=self.month7,
                month8=self.month8,
                month9=self.month9,
                month10=self.month10,
                month11=self.month11,
                month12=self.month12,
                meal1=self.meal1,
                meal2=self.meal2,
                meal3=self.meal3,
                meal4=self.meal4,
                meal5=self.meal5,
                meal6=self.meal6,
                meal7=self.meal7,
                meal8=self.meal8,
                meal9=self.meal9,
                meal10=self.meal10,
                meal11=self.meal11,
                meal12=self.meal12,
                is_online=self.is_online,
                is_delete=self.is_delete,
                ts_update=self.ts_update,
                )
