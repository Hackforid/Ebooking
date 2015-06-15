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
    ota_ids = Column(VARCHAR(50), nullable=False)
