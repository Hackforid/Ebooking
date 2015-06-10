# -*- coding: utf-8 -*-

from tornado.util import ObjectDict

from sqlalchemy import Column, update
from sqlalchemy.dialects.mysql import BIT, INTEGER, VARCHAR, DATETIME, SMALLINT, TINYINT


from models import Base

class ContractMerchantModel(Base):

    __tablename__ = 'contract_merchant'

    __table_args__ = {
        'mysql_charset': 'utf8', 'mysql_engine': 'InnoDB'}

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    merchant_id = Column(INTEGER, nullable=False)
    creator = Column(VARCHAR(50), nullable=False)
    margin = Column(INTEGER, nullable=False)
    receptionist_phone = Column(VARCHAR(50))
    fax = Column(VARCHAR(50), nullable=False)
    cooperation_mode = Column(VARCHAR(50), nullable=False)
    commission = Column(TINYINT, nullable=False)
    settle_cycle = Column(TINYINT, nullable=False, default=0)
    settle_date = Column(TINYINT, nullable=False, default=1)
    settle_order_method = Column(TINYINT, nullable=False, default=0)
    account_name = Column(VARCHAR(50), nullable=False)
    account_bank_name = Column(VARCHAR(50), nullable=False)
    account_bank_id = Column(VARCHAR(50), nullable=False)
    finance_name = Column(VARCHAR(50), nullable=False)
    finance_tel = Column(VARCHAR(50), nullable=False)
    finance_qq = Column(VARCHAR(50), nullable=False)
    business1_name = Column(VARCHAR(50), nullable=False)
    business1_tel = Column(VARCHAR(50), nullable=False)
    business2_name = Column(VARCHAR(50), nullable=False)
    business2_tel = Column(VARCHAR(50), nullable=False)


    @classmethod
    def get_by_merchant_id(cls, session, merchant_id):
        query = session.query(ContractMerchantModel)\
                .filter(ContractMerchantModel.merchant_id == merchant_id,
                        )
        return query.first()


    @classmethod
    def new(cls, session, creator, **kwargs):
        contract = ContractMerchantModel(creator=creator, **kwargs)
        session.add(contract)
        session.commit()
        return contract

    @classmethod
    def update(cls, session, merchant_id, **kwargs):
        session.query(ContractMerchantModel)\
                .filter(ContractMerchantModel.merchant_id == merchant_id,
                        )\
                .update(kwargs)
        session.commit()


    def todict(self):
        return ObjectDict(
                id = self.id,
                merchant_id = self.merchant_id,
                creator = self.creator,
                margin = self.margin,
                receptionist_phone = self.receptionist_phone,
                fax = self.fax,
                cooperation_mode = self.cooperation_mode,
                commission = self.commission,
                settle_cycle = self.settle_cycle,
                settle_date = self.settle_date,
                settle_order_method = self.settle_order_method,
                account_name = self.account_name,
                account_bank_name = self.account_bank_name,
                account_bank_id = self.account_bank_id,
                finance_name = self.finance_name,
                finance_tel = self.finance_tel,
                finance_qq = self.finance_qq,
                business1_name = self.business1_name,
                business1_tel = self.business1_tel,
                business2_name = self.business2_name,
                business2_tel = self.business2_tel,
                )



