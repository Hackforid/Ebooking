# -*- coding: utf-8 -*-

from tornado.util import ObjectDict

from sqlalchemy import Column, update
from sqlalchemy.dialects.mysql import BIT, INTEGER, VARCHAR, DATETIME, SMALLINT, TINYINT


from models import Base

class ContractHotelModel(Base):

    __tablename__ = 'contract_hotel'

    __table_args__ = {
        'mysql_charset': 'utf8', 'mysql_engine': 'InnoDB'}

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    merchant_id = Column(INTEGER, nullable=False)
    hotel_id = Column(INTEGER, nullable=False)
    base_hotel_id = Column(INTEGER, nullable=False)
    weekend = Column(VARCHAR(20), nullable=False, default="5,6")


    @classmethod
    def get_by_hotel(cls, session, hotel_id):
        query = session.query(ContractHotelModel)\
                .filter(ContractHotelModel.hotel_id == hotel_id,
                        )
        return query.first()


    @classmethod
    def new(cls, session, **kwargs):
        contract = ContractHotelModel(**kwargs)
        session.add(contract)
        session.commit()
        return contract

    @classmethod
    def update(cls, session, hotel_id, **kwargs):
        session.query(ContractHotelModel)\
                .filter(ContractHotelModel.hotel_id == hotel_id,
                        )\
                .update(kwargs)
        session.commit()


    def todict(self):
        return ObjectDict(
                id = self.id,
                merchant_id = self.merchant_id,
                hotel_id = self.hotel_id,
                base_hotel_id = self.base_hotel_id,
                weekend = self.weekend,
                )



