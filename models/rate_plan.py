# -*- coding: utf-8 -*-

import datetime
import traceback

from tornado.util import ObjectDict 

from tasks.models import Base
from sqlalchemy import Column
from sqlalchemy.dialects.mysql import BIT, INTEGER, VARCHAR, DATE, TIME, TIMESTAMP, BIGINT, TINYINT

class RatePlanModel(Base):

    __tablename__ = 'ratePlan'
    __table_args__ = {
        'mysql_charset': 'utf8', 'mysql_engine': 'InnoDB'}

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    merchant_id = Column("merchantId", INTEGER, nullable=False, default=0)
    hotel_id = Column("hotelId", INTEGER, nullable=False, default=0)
    roomtype_id = Column("roomTypeId", INTEGER, nullable=False, default=0)
    name = Column(VARCHAR(20), nullable=False)
    pay_types = Column("payType", TINYINT(4), nullable=False, default=1)
    stay_days = Column("stayDays", TINYINT(4), nullable=False, default=1)
    ahead_days = Column("aheadDays", TINYINT(4), nullable=False, default=0)
    cancel_type = Column("cancelType", TINYINT(4), nullable=False, default=1)
    cancel_days = Column("cancelDays", TINYINT(4), nullable=False, default=0)
    cancel_time = Column("cancelTime", TIME)
    punish_type = Column("punishType", TINYINT(4), nullable=False, default=0)
    punish_value = Column("punishValue", INTEGER, nullable=False, default=0)
    guarantee_start_time = Column("guaranteeStartTime", TIME)
    guarantee_type = Column("guaranteeType", TINYINT(4), nullable=False, default=0)
    guarantee_count = Column("guaranteeCount", TINYINT(4), nullable=False, default=0)
    #start_date = Column("startDate", DATE)
    #end_date = Column("endDate", DATE)
    is_online = Column('isOnline', BIT, nullable=False, default=0)
    is_delete = Column('isDelete', BIT, nullable=False, default=0)
    ts_update = Column("tsUpdate", TIMESTAMP)

    @classmethod
    def get_by_id(task_self, id):
        return task_self.session.query(RatePlanModel)\
                .filter(RatePlanModel.id == id)\
                .filter(RatePlanModel.is_delete == 0)\
                .first()

    @classmethod
    def new_rate_plan(cls, session, merchant_id, hotel_id, roomtype_id, name, meal_type, punish_type):
        from models.room_rate import RoomRateModel
        rateplan = RatePlanModel(merchant_id=merchant_id, hotel_id=hotel_id,roomtype_id=roomtype_id, name=name, punish_type=punish_type)
        session.add(rateplan)
        session.commit()

        roomrate = RoomRateModel.new_roomrate(session, hotel_id, roomtype_id, rateplan.id)
        return rateplan, roomrate

    @classmethod
    def get_by_room(cls, session, merchant_id, hotel_id, roomtype_id):
        from models.room_rate import RoomRateModel
        rateplans = session.query(RatePlanModel)\
                .filter(RatePlanModel.merchant_id == merchant_id,
                        RatePlanModel.hotel_id == hotel_id,
                        RatePlanModel.roomtype_id == roomtype_id)\
                .filter(RatePlanModel.is_delete == 0)\
                .all()
        if rateplans:
            roomrates = []
            for rateplan in rateplans:
                roomrate = session.query(RoomRateModel)\
                        .filter(RoomRateModel.rate_plan_id == rateplan.id)\
                        .filter(RoomRateModel.is_delete == 0)\
                        .first()
                if roomrate:
                    roomrates.append(roomrate)

        return rateplans, roomrates

    def todict(self):
        return ObjectDict(
                id=self.id,
                merchant_id=self.merchant_id,
                hotel_id=self.hotel_id,
                roomtype_id=self.roomtype_id,
                name=self.name,
                pay_types=self.pay_types,
                stay_days=self.stay_days,
                ahead_days=self.ahead_days,
                cancel_type=self.cancel_type,
                cancel_days=self.cancel_days,
                cancel_time=self.cancel_time,
                punish_type=self.punish_type,
                punish_value=self.punish_value,
                guarantee_type=self.guarantee_type,
                guarantee_count=self.guarantee_count,
                is_online=self.is_online,
                is_delete=self.is_delete,
                )



