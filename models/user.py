# -*- coding: utf-8 -*-

from models import Base
from sqlalchemy import Column
from sqlalchemy.dialects.mysql import BIT, INTEGER, VARCHAR, DATETIME, BIGINT

class UserModel(Base):

    __tablename__ = 'user'
    __table_args__ = {
    'mysql_charset': 'utf8', 'mysql_engine': 'InnoDB'}

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    merchant_id = Column("merchantId", INTEGER, nullable=False, default=0)
    username = Column(VARCHAR(50), nullable=False)
    nickname = Column(VARCHAR(50), nullable=False)
    password = Column(VARCHAR(50), nullable=False)
    department = Column(VARCHAR(50), nullable=False)
    mobile = Column(VARCHAR(50), nullable=False)
    email = Column(VARCHAR(50), nullable=False)
    authority = Column(BIGINT, nullable=False, default=0)
    is_delete = Column('isDelete', BIT, nullable=False, default=0)

    @classmethod
    def get_user_by_id(cls, session, id):
        return session.query(UserModel).filter(UserModel.id == id, UserModel.is_delete == 0).first()

    @classmethod
    def get_user_by_merchantid_username(cls, session, merchant_id, username):
        return session.query(UserModel)\
            .filter(UserModel.username == username, UserModel.is_delete == 0)\
            .first()

    @classmethod
    def get_user_by_username_and_password(cls, session, username, password):
        return session.query(UserModel)\
            .filter(UserModel.username == username, UserModel.password == password, UserModel.is_delete != 1)\
            .first()
