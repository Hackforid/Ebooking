# -*- coding: utf-8 -*-

from tornado.util import ObjectDict

from sqlalchemy import Column, update
from sqlalchemy.dialects.mysql import BIT, INTEGER, VARCHAR, DATETIME, SMALLINT, TINYINT, TEXT, DATE


from models import Base

class ContractSpecPriceModel(Base):

    __tablename__ = 'contract_spec_price'

    __table_args__ = {
        'mysql_charset': 'utf8', 'mysql_engine': 'InnoDB'}

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    merchant_id = Column(INTEGER, nullable=False)
    hotel_id = Column(INTEGER, nullable=False)
    roomtype_id = Column(INTEGER, nullable=False)
    pay_type = Column(TINYINT, nullable=False, default=0)
    start_date = Column(DATE, nullable=False)
    end_date = Column(DATE, nullable=False)
    price = Column(INTEGER, nullable=False, default=0)
    remark = Column(VARCHAR(200))
    is_delete = Column(BIT(1), nullable=False, default=0)
