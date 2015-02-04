# -*- coding: utf-8 -*-

import datetime

from tornado.util import ObjectDict

from sqlalchemy import Column
from sqlalchemy.dialects.mysql import BIT, INTEGER, VARCHAR, DATETIME, BIGINT, TINYINT, DATE


from models import Base
from constants import OTA

class IncomeModel(Base):

    __tablename__ = 'income'
    __table_args__ = {
        'mysql_charset': 'utf8', 'mysql_engine': 'InnoDB'}

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    merchant_id = Column("merchantId", INTEGER(unsigned=True), nullable=False, default=0)
    pay_type = Column("payType", TINYINT(4), default=1, nullable=True)
    ota_id = Column("otaId", INTEGER(unsigned=True), default=0, nullable=False)
    create_date = Column("createDate", DATE, nullable=False)
    value = Column(INTEGER, default=0, nullable=False)
    remark = Column(VARCHAR(100))
    is_delete = Column('isDelete', BIT, nullable=False, default=0)

    @property
    def ota_name(self):
        return OTA.get(self.ota_id, '')

    @classmethod
    def get_by_id(self, session, id):
        return session.query(IncomeModel)\
                .filter(IncomeModel.id == id)\
                .filter(IncomeModel.is_delete == 0)\
                .first()


    @classmethod
    def get_in_month(self, session, merchant_id, year, month, pay_type, ota_id=None):
        date_start = datetime.date(year, month, 1)
        if month == 12:
            month = 1
            year = year + 1
        else:
            month = month + 1
        date_end = datetime.date(year, month, 1)

        query = session.query(IncomeModel.merchant_id == merchant_id,
                IncomeModel.create_date >= date_start,
                IncomeModel.create_date <= date_end,
                IncomeModel.pay_type == pay_type,
                IncomeModel.is_delete == 0)

        if ota_id is not None:
            query = query.filter(IncomeModel.ota_id == ota_id)

        return query.all()

    def todict(self):
        return ObjectDict(
                id=self.id,
                merchant_id=self.merchant_id,
                pay_type=self.pay_type,
                ota_id=self.ota_id,
                ota_name=self.ota_name,
                create_date=self.create_date,
                value=self.value,
                remark=self.remark,
                is_delete=self.is_delete,
                )
