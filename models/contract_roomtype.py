# -*- coding: utf-8 -*-

from tornado.util import ObjectDict

from sqlalchemy import Column, update
from sqlalchemy.dialects.mysql import BIT, INTEGER, VARCHAR, DATETIME, SMALLINT, TINYINT, TEXT


from models import Base

class ContractRoomTypeModel(Base):

    __tablename__ = 'contract_roomtype'

    __table_args__ = {
        'mysql_charset': 'utf8', 'mysql_engine': 'InnoDB'}

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    merchant_id = Column(INTEGER, nullable=False)
    hotel_id = Column(INTEGER, nullable=False)
    base_hotel_id = Column(INTEGER, nullable=False)
    roomtype_id = Column(INTEGER, nullable=False)
    base_roomtype_id = Column(INTEGER, nullable=False)
    pay_type = Column(TINYINT, nullable=False, default=0)
    weekday_base_price = Column(INTEGER)
    weekend_base_price = Column(INTEGER)
    weekday_sell_price = Column(INTEGER)
    weekend_sell_price = Column(INTEGER)
    retain_num = Column(INTEGER)
    breakfest = Column(VARCHAR(50))
    remark = Column(TEXT)
    is_delete = Column(BIT(1), nullable=False, default=0)

    @classmethod
    def get_by_hotel(cls, session, hotel_id):
        query = session.query(ContractRoomTypeModel)\
                .filter(ContractRoomTypeModel.hotel_id == hotel_id,
                        ContractRoomTypeModel.is_delete == 0)
        return query.all()

    def todict(self):
        return ObjectDict(
                id = self.id,
                merchant_id = self.merchant_id,
                hotel_id = self.hotel_id,
                base_hotel_id = self.base_hotel_id,
                roomtype_id = self.roomtype_id,
                base_roomtype_id = self.base_roomtype_id,
                pay_type = self.pay_type,
                weekday_base_price = self.weekday_base_price,
                weekend_base_price = self.weekend_base_price,
                weekday_sell_price = self.weekday_sell_price,
                weekend_sell_price = self.weekend_sell_price,
                retain_num = self.retain_num,
                breakfest = self.breakfest,
                remark = self.remark,
                )
