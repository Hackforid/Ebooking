# -*- coding: utf-8 -*-

from tornado.util import ObjectDict

from sqlalchemy import Column, update
from sqlalchemy.dialects.mysql import BIT, INTEGER, VARCHAR, DATETIME, SMALLINT


from models import Base

class ContractModel(Base):

    __tablename__ = 'contract'
    __table_args__ = {
        'mysql_charset': 'utf8', 'mysql_engine': 'InnoDB'}

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(50), nullable=False)
    type = Column(SMALLINT(2), nullable=False, default=1)
    commission = Column(SMALLINT(3), nullable=False, default=0)
    bank_name = Column("bankName", VARCHAR(50), nullable=False)
    bank_account_id = Column("bankAccountId", VARCHAR(50), nullable=False)
    bank_account_name = Column("bankAccountName", VARCHAR(50), nullable=False)
    merchant_id = Column("merchantId", INTEGER, nullable=False, default=0)
    is_delete = Column('isDelete', BIT, nullable=False, default=0)

    PAY_TYPE_ARRIVE = 0
    PAY_TYPE_PRE = 1

    @classmethod
    def get_by_id(cls, session, id):
        query = session.query(ContractModel)\
                .filter(ContractModel.id == id)\
                .filter(ContractModel.is_delete == 0)
        return query.first()

    @classmethod
    def get_by_id_and_merchant(cls, session, id, merchant_id):
        query = session.query(ContractModel)\
                .filter(ContractModel.id == id)\
                .filter(ContractModel.merchant_id == merchant_id)\
                .filter(ContractModel.is_delete == 0)
        return query.first()

    @classmethod
    def get_by_merchant(cls, session, merchant_id):
        query = session.query(ContractModel)\
                .filter(ContractModel.merchant_id == merchant_id)\
                .filter(ContractModel.is_delete == 0)
        return query.all()

    @classmethod
    def get_by_merchant_and_type(cls, session, merchant_id, type):
        query = session.query(ContractModel)\
                .filter(ContractModel.merchant_id == merchant_id,
                        ContractModel.type == type)\
                .filter(ContractModel.is_delete == 0)
        return query.first()


    @classmethod
    def new(cls, session, merchant_id, name, type, commission, bank_name, bank_account_id, bank_account_name):
        contract = ContractModel(merchant_id=merchant_id, name=name, type=type, commission=commission, bank_name=bank_name, bank_account_id=bank_account_id, bank_account_name=bank_account_name)
        session.add(contract)
        session.commit()
        return contract

    def todict(self):
        return ObjectDict(
                id=self.id,
                merchant_id=self.merchant_id,
                name=self.name,
                type=self.type,
                commission=self.commission,
                bank_name=self.bank_name,
                bank_account_id=self.bank_account_id,
                bank_account_name=self.bank_account_name,
                is_delete=self.is_delete)
