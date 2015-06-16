# -*- coding: utf-8 -*-

from tornado.util import ObjectDict

from sqlalchemy import Column, update
from sqlalchemy.dialects.mysql import BIT, INTEGER, VARCHAR, DATETIME, SMALLINT


from models import Base

class OtaChannelModel(Base):

    __tablename__ = 'ota_channel'
    __table_args__ = {
        'mysql_charset': 'utf8', 'mysql_engine': 'InnoDB'}

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    hotel_id = Column(INTEGER, nullable=False)
    ota_ids = Column(VARCHAR(50), nullable=False, default='0')

    @classmethod
    def get_by_hotel_id(cls, session, hotel_id):
        query = session.query(OtaChannelModel)\
                .filter(OtaChannelModel.hotel_id == hotel_id)
        return query.first()

    @classmethod
    def get_by_hotel_ids(cls, session, hotel_ids):
        query = session.query(OtaChannelModel)\
                .filter(OtaChannelModel.hotel_id.in_(hotel_ids))
        return query.all()

    def get_ota_ids(self):
        ota_ids = self.ota_ids.split(',')
        return [int(id) for id in ota_ids]


    def todict(self):
        return ObjectDict(
                id=self.id,
                hotel_id=self.hotel_id,
                ota_ids=self.ota_ids,
                )
