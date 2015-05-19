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
    hotel_id = Column(INTEGER, nullable=False)
    roomtype_id = Column(INTEGER, nullable=False)
    pay_type = Column(TINYINT, nullable=False, default=0)
    start_date = Column(DATE, nullable=False)
    end_date = Column(DATE, nullable=False)
    price = Column(INTEGER, nullable=False, default=0)
    remark = Column(VARCHAR(200))
    is_delete = Column(BIT(1), nullable=False, default=0)

    @classmethod
    def get_by_id(cls, session, id):
        query = session.query(ContractSpecPriceModel)\
                .filter(ContractSpecPriceModel.id == id,
                        ContractSpecPriceModel.is_delete == 0
                        )
        return query.first()


    @classmethod
    def get_by_hotel(cls, session, hotel_id):
        query = session.query(ContractSpecPriceModel)\
                .filter(ContractSpecPriceModel.hotel_id == hotel_id,
                        ContractSpecPriceModel.is_delete == 0
                        )
        return query.all()

    @classmethod
    def get_by_hotel_roomtype_pay_type(cls, session, hotel_id, roomtype_id, pay_type):
        query = session.query(ContractSpecPriceModel)\
                .filter(ContractSpecPriceModel.hotel_id == hotel_id,
                        ContractSpecPriceModel.roomtype_id == roomtype_id,
                        ContractSpecPriceModel.pay_type == pay_type,
                        ContractSpecPriceModel.is_delete == 0
                        )
        return query.all()

    @classmethod
    def new(cls, session, hotel_id, roomtype_id, pay_type, **kwargs):
        contract = ContractSpecPriceModel(hotel_id=hotel_id, roomtype_id=roomtype_id, pay_type=pay_type, **kwargs)
        session.add(contract)
        session.commit()
        return contract

    @classmethod
    def update(cls, session, id, **kwargs):
        session.query(ContractSpecPriceModel)\
                .filter(ContractSpecPriceModel.id == id)\
                .update(kwargs)
        session.commit()


    def todict(self):
        return ObjectDict(
                id = self.id,
                hotel_id = self.hotel_id,
                roomtype_id = self.roomtype_id,
                pay_type = self.pay_type,
                start_date = self.start_date,
                end_date = self.end_date,
                price = self.price,
                remark = self.remark,
                )
