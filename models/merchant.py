# -*- coding: utf-8 -*-

from tornado.util import ObjectDict 

from models import Base
from sqlalchemy import Column, DateTime
from sqlalchemy.dialects.mysql import BIT, INTEGER, VARCHAR, DATETIME, BIGINT, TINYINT
from tools.auth import md5_password


class MerchantModel(Base):

    __tablename__ = 'merchant'
    __table_args__ = {
        'mysql_charset': 'utf8', 'mysql_engine': 'InnoDB'}

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(50), nullable=False)
    type = Column(TINYINT(3), nullable=False, default=0)
    is_online = Column('isOnline', BIT, nullable=False, default=0)
    is_delete = Column('isDelete', BIT, nullable=False, default=0)

    @classmethod
    def get_by_id(cls, session, id):
        return session.query(MerchantModel).filter(MerchantModel.id == id, MerchantModel.is_delete == 0).first()
