# -*- coding: utf-8 -*-

import datetime
import traceback

from tornado.util import ObjectDict 

from tasks.models import Base
from sqlalchemy import Column
from sqlalchemy.dialects.mysql import BIT, INTEGER, VARCHAR, DATE, TIME, TEXT, TIMESTAMP, BIGINT, TINYINT

from tasks.celery_app import app
from tasks.base_task import SqlAlchemyTask

class OrderModel(Base):

    __tablename__ = 'order'
    __table_args__ = {
        'mysql_charset': 'utf8', 'mysql_engine': 'InnoDB'}

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    main_order_id = Column('mainOrderId', INTEGER, nullable=False)
    merchant_id = Column("merchantId", INTEGER, nullable=False, default=0)
    hotel_id = Column("hotelId", INTEGER, nullable=False, default=0)
    hotel_name = Column("hotelName", VARCHAR(50), nullable=False)
    room_type_id = Column("roomTypeId", INTEGER, nullable=False, default=0)
    room_type_name = Column("roomTypeName", VARCHAR(50), nullable=False)
    rate_plan_id = Column("ratePlanId", INTEGER, nullable=False, default=0)
    rate_plan_name = Column("ratePlanName", VARCHAR(50), nullable=False)
    room_num = Column("roomNum", INTEGER, nullable=False, default=0)
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

    @staticmethod
    @app.task(base=SqlAlchemyTask, bind=True)
    def get_by_main_order_id(task_self, main_order_id):
        order = task_self.session.query(OrderModel)\
                .filter(OrderModel.main_order_id==main_order_id)\
                .first()
        return order
    
    @staticmethod
    @app.task(base=SqlAlchemyTask, bind=True)
    def new_order(task_self, submit_order):
        print '*' * 10
        print submit_order
        order = OrderModel(
                main_order_id=submit_order.id,
                merchant_id=submit_order.merchant_id,
                hotel_id=submit_order.hotel_id,
                hotel_name=submit_order.hotel_name,
                room_type_id=submit_order.room_type_id,
                room_type_name=submit_order.room_type_name,
                rate_plan_id=submit_order.rate_plan_id,
                rate_plan_name=submit_order.rate_plan_name,
                room_num=submit_order.room_quantity,
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
                status=submit_order.status,
                total_price=submit_order.chain_total_price,
                everyday_price=submit_order.base_price,
                create_time=submit_order.create_time,
                update_time=submit_order.update_time,
                #create_time=datetime.datetime.today(),
                #update_time=datetime.datetime.today(),
                extra=submit_order.extra
                )
        task_self.session.add(order)
        task_self.session.commit()

        print 'create order', order.todict()
        return order



    def todict(self):
        return ObjectDict(
                id=self.id,
                main_order_id=self.main_order_id,
                hotel_id=self.hotel_id,
                hotel_name=self.hotel_name,
                room_type_id=self.room_type_id,
                room_type_name=self.room_type_name,
                rate_plan_id=self.rate_plan_id,
                rate_plan_name=self.rate_plan_name,
                room_num=self.room_num,
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
                )
