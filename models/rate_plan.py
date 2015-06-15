# -*- coding: utf-8 -*-

import datetime
import traceback

from tornado.util import ObjectDict 

from models import Base
from sqlalchemy import Column
from sqlalchemy.dialects.mysql import BIT, INTEGER, VARCHAR, DATE, TIME, TIMESTAMP, BIGINT, TINYINT

class RatePlanModel(Base):

    __tablename__ = 'ratePlan'
    __table_args__ = {
        'mysql_charset': 'utf8', 'mysql_engine': 'InnoDB'}

    PAY_TYPE_ARRIVE = 0
    PAY_TYPE_PRE = 1

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    merchant_id = Column("merchantId", INTEGER, nullable=False, default=0)
    hotel_id = Column("hotelId", INTEGER, nullable=False, default=0)
    roomtype_id = Column("roomTypeId", INTEGER, nullable=False, default=0)
    base_hotel_id = Column("baseHotelId", INTEGER, nullable=False, default=0)
    base_roomtype_id = Column("baseRoomTypeId", INTEGER, nullable=False, default=0)
    name = Column(VARCHAR(20), nullable=False)
    pay_type = Column("payType", TINYINT(4), nullable=False, default=1)
    stay_days = Column("stayDays", TINYINT(4), nullable=False, default=1)
    ahead_days = Column("aheadDays", TINYINT(4), nullable=False, default=0)
    cancel_type = Column("cancelType", TINYINT(4, unsigned=True), nullable=False, default=1)
    cancel_days = Column("cancelDays", TINYINT(4), nullable=False, default=0)
    cancel_time = Column("cancelTime", TIME, nullable=False, default="18:00:00")
    punish_type = Column("punishType", TINYINT(4, unsigned=True), nullable=False, default=0)
    punish_value = Column("punishValue", INTEGER(unsigned=True), nullable=False, default=0)
    guarantee_start_time = Column("guaranteeStartTime", TIME, default="00:00:00")
    guarantee_type = Column("guaranteeType", TINYINT(4), nullable=False, default=0)
    guarantee_count = Column("guaranteeCount", TINYINT(4), nullable=False, default=0)
    start_date = Column("startDate", DATE, nullable=False, default='1990-09-21')
    end_date = Column("endDate", DATE, nullable=False, default='3000-12-25')
    is_online = Column('isOnline', BIT, nullable=False, default=1)
    is_delete = Column('isDelete', BIT, nullable=False, default=0)
    ts_update = Column("tsUpdate", TIMESTAMP)

    @classmethod
    def get_by_id(cls, session, id, with_delete=False):
        query = session.query(RatePlanModel)\
                .filter(RatePlanModel.id == id)
        if not with_delete:
            query = query.filter(RatePlanModel.is_delete == 0)
        return query.first()

    @classmethod
    def get_by_ids(cls, session, ids, with_delete=False):
        query = session.query(RatePlanModel)\
                .filter(RatePlanModel.id.in_(ids))
        if with_delete:
            return query.all()
        else:
            return query.filter(RatePlanModel.is_delete == 0).all()

    @classmethod
    def get_by_merchant_hotel_room_name(cls, session, merchant_id, hotel_id, roomtype_id, name):
        return session.query(RatePlanModel)\
                .filter(RatePlanModel.merchant_id == merchant_id,
                        RatePlanModel.hotel_id == hotel_id,
                        RatePlanModel.roomtype_id == roomtype_id,
                        RatePlanModel.name == name)\
                .filter(RatePlanModel.is_delete == 0)\
                .first()

    @classmethod
    def get_by_roomtype(cls, session, roomtype_id):
        return session.query(RatePlanModel)\
                .filter(RatePlanModel.roomtype_id == roomtype_id)\
                .filter(RatePlanModel.is_delete == 0)\
                .all()

    @classmethod
    def get_by_merchant(cls, session, merchant_id, with_delete=False):
        query = session.query(RatePlanModel)\
                .filter(RatePlanModel.merchant_id == merchant_id)
        if not with_delete:
            query = query.filter(RatePlanModel.is_delete == 0)
        return query.all()

    @classmethod
    def get_by_id_with_merchant(cls, session, id, merchant_id):
        return session.query(RatePlanModel)\
                .filter(RatePlanModel.id == id)\
                .filter(RatePlanModel.merchant_id == merchant_id)\
                .filter(RatePlanModel.is_delete == 0)\
                .first()


    @classmethod
    def new_rate_plan(cls, session, merchant_id, hotel_id, roomtype_id, base_hotel_id, base_roomtype_id, name, meal_num, punish_type, ahead_days, stay_days, pay_type=None, guarantee_type=None, guarantee_start_time=None, commit=True):

        if pay_type == cls.PAY_TYPE_PRE:
            rateplan = RatePlanModel(merchant_id=merchant_id, hotel_id=hotel_id,roomtype_id=roomtype_id, base_hotel_id=base_hotel_id, base_roomtype_id=base_roomtype_id, name=name, punish_type=punish_type)
        else:
            rateplan = RatePlanModel(merchant_id=merchant_id, hotel_id=hotel_id,roomtype_id=roomtype_id, base_hotel_id=base_hotel_id, base_roomtype_id=base_roomtype_id, name=name, punish_type=punish_type, pay_type=pay_type, guarantee_start_time=guarantee_start_time, guarantee_type=guarantee_type)

        if ahead_days is not None:
            rateplan.ahead_days = ahead_days
        if stay_days is not None:
            rateplan.stay_days = stay_days

        session.add(rateplan)
        if commit:
            session.commit()
        return rateplan

    @classmethod
    def get_by_room(cls, session, merchant_id, hotel_id, roomtype_id):
        rateplans = session.query(RatePlanModel)\
                .filter(RatePlanModel.merchant_id == merchant_id,
                        RatePlanModel.roomtype_id == roomtype_id,
                        RatePlanModel.hotel_id == hotel_id)\
                .filter(RatePlanModel.is_delete == 0)\
                .all()
        return rateplans

    def todict(self):
        return ObjectDict(
                id=self.id,
                merchant_id=self.merchant_id,
                hotel_id=self.hotel_id,
                roomtype_id=self.roomtype_id,
                base_hotel_id=self.base_hotel_id,
                base_roomtype_id=self.base_roomtype_id,
                name=self.name,
                pay_type=self.pay_type,
                stay_days=self.stay_days,
                ahead_days=self.ahead_days,
                cancel_type=self.cancel_type,
                cancel_days=self.cancel_days,
                cancel_time=self.cancel_time,
                punish_type=self.punish_type,
                punish_value=self.punish_value,
                guarantee_start_time=self.guarantee_start_time,
                guarantee_type=self.guarantee_type,
                guarantee_count=self.guarantee_count,
                start_date=self.start_date,
                end_date=self.end_date,
                is_online=self.is_online,
                is_delete=self.is_delete,
                )



