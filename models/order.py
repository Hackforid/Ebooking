# -*- coding: utf-8 -*-

import time
import datetime
import json

from tornado.util import ObjectDict 

from models import Base
from sqlalchemy import Column
from sqlalchemy.dialects.mysql import BIT, INTEGER, VARCHAR, DATE, TIME, TEXT, TIMESTAMP, BIGINT, TINYINT

class OrderModel(Base):

    __tablename__ = 'order'
    __table_args__ = {
        'mysql_charset': 'utf8', 'mysql_engine': 'InnoDB'}

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    main_order_id = Column('mainOrderId', INTEGER, nullable=False)
    merchant_id = Column("merchantId", INTEGER, nullable=False, default=0)
    hotel_id = Column("hotelId", INTEGER, nullable=False, default=0)
    hotel_name = Column("hotelName", VARCHAR(50), nullable=False)
    roomtype_id = Column("roomTypeId", INTEGER, nullable=False, default=0)
    roomtype_name = Column("roomTypeName", VARCHAR(50), nullable=False)
    rateplan_id = Column("ratePlanId", INTEGER, nullable=False, default=0)
    rateplan_name = Column("ratePlanName", VARCHAR(50), nullable=False)
    room_num = Column("roomNum", INTEGER, nullable=False, default=0)
    room_num_record = Column("roomNumRecord", VARCHAR(500), nullable=False)
    currency_type = Column("currencyType", VARCHAR(10), nullable=False, default="CNY")
    pay_type = Column("payType", INTEGER, nullable=False, default=0)
    bed_type = Column("bedType", INTEGER, nullable=False, default=0)
    checkin_date = Column("checkInDate", DATE, nullable=False)
    checkout_date = Column("checkOutDate", DATE, nullable=False)
    arrival_time = Column("arrivalTime", TIME, nullable=False, default="18:00:00")
    contact_name = Column("contactName", VARCHAR(30), nullable=False)
    contact_mobile = Column("contactMobile", VARCHAR(50), nullable=False)
    contact_email = Column("contactEmail", VARCHAR(50), nullable=False)
    customer_num = Column("customerNum", INTEGER, nullable=False, default=0)
    customer_info = Column("customerInfo", TEXT, nullable=False)
    customer_remark = Column("customerRemark", TEXT, nullable=False)
    breakfast = Column(VARCHAR(100), nullable=False)
    guarantee_info = Column("guaranteeInfo", TEXT, nullable=False)
    status = Column(INTEGER, nullable=False)
    total_price = Column("totalPrice", INTEGER, nullable=False)
    everyday_price = Column("everydayPrice", VARCHAR(200), nullable=False)
    extra = Column(TEXT, nullable=False)
    create_time = Column("createTime", TIMESTAMP)
    update_time = Column("updateTime", TIMESTAMP)
    confirm_type = Column("confirmType", TINYINT(1), nullable=False, default=0)
    cancel_type = Column("cancelType", TINYINT(4, unsigned=True), nullable=False, default=1)
    punish_type = Column("punishType", TINYINT(4, unsigned=True), nullable=False, default=0)
    punish_value = Column("punishValue", INTEGER(unsigned=True), nullable=False, default=0)
    guarantee_start_time = Column("guaranteeStartTime", TIME, default="00:00:00")
    guarantee_type = Column("guaranteeType", TINYINT(4), nullable=False, default=0)
    ota_id = Column('otaId', INTEGER, nullable=False, default=0)
    ota_name = Column('otaName', VARCHAR(50), nullable=False, default='')
    exception_info = ''

    CONFIRM_TYPE_INIT = 0
    CONFIRM_TYPE_AUTO = 1
    CONFIRM_TYPE_MANUAL = 2

    @classmethod
    def search(cls, session, merchant_id, id=None, hotel_name=None, checkin_date_start=None, checkin_date_end=None, customer=None, status=None, create_time_start=None, create_time_end=None, start=None, limit=None):
        if id:
            order = cls.get_by_id(session, id)
            if order:
                return [order], 1
            else:
                return None, 0
        query = session.query(OrderModel).filter(OrderModel.merchant_id==merchant_id)

        if hotel_name:
            query = query.filter(OrderModel.hotel_name.like(u'%{}%'.format(hotel_name)))
        if customer:
            query = query.filter(OrderModel.customer_info.like(u'%{}%'.format(customer)))
        if checkin_date_start:
            date = datetime.datetime.strptime(checkin_date_start, '%Y-%m-%d')
            query = query.filter(OrderModel.checkin_date >= date.date())
        if checkin_date_end:
            date = datetime.datetime.strptime(checkin_date_end, '%Y-%m-%d')
            query = query.filter(OrderModel.checkin_date <= date.date())
        if status is not None:
            if isinstance(status, list):
                query = query.filter(OrderModel.status.in_(status))
            else:
                query = query.filter(OrderModel.status == status)
        if create_time_start:
            date = datetime.datetime.strptime(create_time_start, '%Y-%m-%d')
            query = query.filter(OrderModel.create_time >= date)
        if create_time_end:
            date = datetime.datetime.strptime(create_time_end, '%Y-%m-%d')
            date = date + datetime.timedelta(days=1)
            query = query.filter(OrderModel.create_time <= date)

        total = query.count()

        if start:
            query = query.offset(start)
        if limit:
            query = query.limit(limit)

        return query.all(), total

    @classmethod
    def get_success_order_by_checkout_date_in_month(self, session, merchant_id, year, month, pay_type, ota_ids=None):
        date_start = datetime.date(year, month, 1)
        if month == 12:
            month = 1
            year = year + 1
        else:
            month = month + 1
        date_end = datetime.date(year, month, 1)
        
        query = session.query(OrderModel)\
                .filter(OrderModel.merchant_id == merchant_id)\
                .filter(OrderModel.status == 300)\
                .filter(OrderModel.checkout_date >= date_start,
                        OrderModel.checkout_date < date_end)\
                .filter(OrderModel.pay_type == pay_type)
        if ota_ids is not None:
            query = query.filter(OrderModel.ota_id.in_(ota_ids))

        return query.all()

    @classmethod
    def get_by_id(cls, session, id):
        order = session.query(OrderModel)\
                .filter(OrderModel.id == id)\
                .first()
        return order

    @classmethod
    def get_by_merchant_and_id(cls, session, merchant_id, id):
        order = session.query(OrderModel)\
                .filter(OrderModel.id == id)\
                .filter(OrderModel.merchant_id == merchant_id)\
                .first()
        return order

    @classmethod
    def get_by_main_order_id(cls, session, main_order_id):
        order = session.query(OrderModel)\
                .filter(OrderModel.main_order_id==main_order_id)\
                .first()
        return order

    @classmethod
    def change_order_status_by_main_order_id(cls, session, main_order_id, status):
        session.query(OrderModel)\
                .filter(OrderModel.main_order_id==main_order_id)\
                .update({'status': status})
        session.commit()

    @classmethod
    def new_order(cls, session, submit_order):
        from models.rate_plan import  RatePlanModel
        order = OrderModel(
                main_order_id=submit_order.id,
                merchant_id=submit_order.merchant_id,
                hotel_id=submit_order.hotel_id,
                hotel_name=submit_order.hotel_name,
                roomtype_id=submit_order.roomtype_id,
                roomtype_name=submit_order.roomtype_name,
                rateplan_id=submit_order.rateplan_id,
                rateplan_name=submit_order.rateplan_name,
                room_num=submit_order.room_quantity,
                room_num_record='',
                currency_type=submit_order.currency_type,
                pay_type=submit_order.pay_type,
                bed_type=submit_order.bed_type,
                checkin_date=submit_order.checkin_date,
                checkout_date=submit_order.checkout_date,
                arrival_time=submit_order.last_arrive_time,
                contact_name=submit_order.contact_name,
                contact_email=submit_order.contact_email,
                contact_mobile=submit_order.contact_mobile,
                customer_num=submit_order.customer_quantity,
                customer_info=submit_order.customer_info,
                customer_remark=submit_order.customer_remark,
                breakfast=submit_order.breakfast,
                guarantee_info=submit_order.guarantee_info,
                status=0,
                total_price=submit_order.base_total_price,
                everyday_price=submit_order.base_price,
                extra=submit_order.extra,
                punish_type=submit_order.punish_type,
                punish_value=submit_order.punish_value,
                cancel_type=submit_order.cancel_type,
                ota_id=submit_order.ota_id,
                ota_name=submit_order.ota_name
                )
        if submit_order.pay_type == RatePlanModel.PAY_TYPE_ARRIVE:
            order.guarantee_type = submit_order.guarantee_type
            order.guarantee_start_time = submit_order.guarantee_start_time
        session.add(order)
        session.commit()

        return order

    @classmethod
    def get_waiting_orders(cls, session, merchant_id, start=None, limit=None):
        query = session.query(OrderModel)\
                .filter(OrderModel.merchant_id == merchant_id)\
                .filter(OrderModel.status == 100)
        total = query.count()

        if start:
            query = query.offset(start)
        if limit:
            query = query.limit(limit)

        return query.all(), total

    @classmethod
    def get_waiting_orders_count(cls, session, merchant_id):
        query = session.query(OrderModel)\
                .filter(OrderModel.merchant_id == merchant_id)\
                .filter(OrderModel.status == 100)
        total = query.count()

        return total


    @classmethod
    def get_today_book_orders(cls, session, merchant_id, start=None, limit=None):
        today = datetime.date.today()
        query = session.query(OrderModel)\
                .filter(OrderModel.merchant_id == merchant_id,
                        OrderModel.create_time >= today,
                        OrderModel.status.in_([100, 300, 400, 500, 600])
                        )
        total = query.count()

        if start:
            query = query.offset(start)
        if limit:
            query = query.limit(limit)

        return query.all(), total

    @classmethod
    def get_today_checkin_orders(cls, session, merchant_id, start=None, limit=None):
        today = datetime.date.today()
        tomorrow = today + datetime.timedelta(days=1)
        query = session.query(OrderModel)\
                .filter(OrderModel.merchant_id == merchant_id,
                        OrderModel.checkin_date >= today,
                        OrderModel.checkin_date < tomorrow,
                        OrderModel.status.in_([100, 300, 400, 500, 600])
                        )
        total = query.count()
        if start:
            query = query.offset(start)
        if limit:
            query = query.limit(limit)

        all = query.all()
        return all, total

    def confirm_by_user(self, session):
        self.status = 300
        session.commit()

    def get_has_breakfast(self):
        if self.breakfast:
            breakfasts = self.breakfast.split(',')
            if breakfasts[0] != '0':
                return True
        return False

    def get_stay_days(self):
        return (self.checkout_date - self.checkin_date).days

    def todict(self):
        return ObjectDict(
                id=self.id, main_order_id=self.main_order_id,
                hotel_id=self.hotel_id,
                hotel_name=self.hotel_name,
                roomtype_id=self.roomtype_id,
                roomtype_name=self.roomtype_name,
                rateplan_id=self.rateplan_id,
                rateplan_name=self.rateplan_name,
                room_num=self.room_num,
                room_num_record=self.room_num_record,
                currency_type=self.currency_type,
                pay_type=self.pay_type,
                bed_type=self.bed_type,
                checkin_date=self.checkin_date,
                checkout_date=self.checkout_date,
                arrival_time=self.arrival_time,
                contact_name=self.contact_name,
                contact_email=self.contact_email,
                contact_mobile=self.contact_mobile,
                customer_info=self.customer_info,
                customer_num=self.customer_num,
                customer_remark=self.customer_remark,
                breakfast=self.breakfast,
                guarantee_info=self.guarantee_info,
                status=self.status,
                total_price=self.total_price,
                everyday_price=self.everyday_price,
                extra=self.extra,
                create_time=self.create_time,
                confirm_type=self.confirm_type,
                cancel_type=self.cancel_type,
                punish_type=self.punish_type,
                punish_value=self.punish_value,
                guarantee_type=self.guarantee_type,
                guarantee_start_time=self.guarantee_start_time,
                ota_id=self.ota_id,
                ota_name=self.ota_name,
                stay_days=self.get_stay_days(),
                has_breakfast=self.get_has_breakfast(),
                exception_info=self.exception_info,
                )
