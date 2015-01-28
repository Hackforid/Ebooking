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
    is_online = Column('isOnline', BIT, nullable=False, default=1)
    is_delete = Column('isDelete', BIT, nullable=False, default=0)
    is_suspend = Column('isSuspend', BIT, nullable=False, default=0)

    TYPE_TRAVEL_AGENCY = 0
    TYPE_MONOMER_HOTEL = 1

    @classmethod
    def get_by_id(cls, session, id):
        return session.query(MerchantModel).filter(MerchantModel.id == id, MerchantModel.is_delete == 0).first()

    @classmethod
    def get_all(cls, session):
        return session.query(MerchantModel)\
                .filter(MerchantModel.is_delete == 0)\
                .all()

    @classmethod
    def new_merchant(cls, session, name, type):
        merchant = MerchantModel(name=name, type=type)
        session.add(merchant)
        session.commit()
        return merchant

    def update(self, session, name, type):
        if name:    
            self.name = name
        if int(type) in [self.TYPE_TRAVEL_AGENCY, self.TYPE_MONOMER_HOTEL]:
            self.type = int(type)
        session.commit()

    def todict(self):
        return ObjectDict(
                id=self.id,
                name=self.name,
                type=self.type,
                is_online=self.is_online,
                is_delete=self.is_delete,
                is_suspend=self.is_suspend,
                )
