# -*- coding: utf-8 -*-

import datetime

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
    def new_roomrate(cls, session, hotel_id, roomtype_id, rate_plan_id, commit=True):
        room = RoomRateModel(hotel_id=hotel_id,
                             roomtype_id=roomtype_id, rate_plan_id=rate_plan_id)
        session.add(room)
        if commit:
            session.commit()

        return room

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
                is_online=self.is_online,
                is_delete=self.is_delete,
                ts_update=self.ts_update,
                )
