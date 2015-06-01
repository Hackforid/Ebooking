# -*- coding: utf-8 -*-

import datetime

from tornado.util import ObjectDict

from models import Base
from sqlalchemy import Column
from sqlalchemy.dialects.mysql import BIT, INTEGER, VARCHAR, DATETIME, BIGINT

class OrderHistoryModel(Base):

    __tablename__ = 'orderHistory'
    __table_args__ = {
        'mysql_charset': 'utf8', 'mysql_engine': 'InnoDB'}

    id = Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    merchant_id = Column("merchantId", INTEGER(unsigned=True), nullable=False, default=0)
    order_id = Column("orderId", INTEGER(unsigned=True), nullable=False, default=0)
    pre_status = Column("preStatus", INTEGER(unsigned=True), nullable=False, default=0)
    status = Column(INTEGER(unsigned=True), nullable=False, default=0)
    user_id = Column("userId", INTEGER(unsigned=True), nullable=False, default=0)
    username = Column(VARCHAR(50), nullable=False, default='0')
    extra = Column(VARCHAR(50), nullable=False)

    @classmethod
    def get_by_id(cls, session, id):
        return session.query(OrderHistoryModel)\
                .filter(OrderHistoryModel.id == id).first()

    @classmethod
    def set_order_status_by_server(cls, session, order, pre_status, new_status):
        history = OrderHistoryModel(merchant_id=order.merchant_id, order_id=order.id, pre_status=pre_status, status=new_status, user_id=0, username="server", extra="operate by server")
        session.add(history)
        session.commit()

    @classmethod
    def set_order_status_by_user(cls, session, user, order, pre_status, new_status):
        history = OrderHistoryModel(merchant_id=order.merchant_id, order_id=order.id, pre_status=pre_status, status=new_status, user_id=user.id, username=user.username, extra="operate by user")
        session.add(history)
        session.commit()

    @classmethod
    def get_lock_test(cls, session, id):
        query = session.query(OrderHistoryModel)\
                .filter(OrderHistoryModel.id == id)\
                .with_for_update()

        return query.first()
