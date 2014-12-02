# -*- coding: utf-8 -*-

from tornado.util import ObjectDict 

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
    is_valid = Column('isValid', BIT, nullable=False, default=1)
    is_delete = Column('isDelete', BIT, nullable=False, default=0)

    @classmethod
    def get_user_by_id(cls, session, id):
        return session.query(UserModel).filter(UserModel.id == id, UserModel.is_delete == 0).first()

    @classmethod
    def get_user_by_merchantid_username(cls, session, merchant_id, username):
        return session.query(UserModel)\
            .filter(UserModel.username == username, UserModel.merchant_id == merchant_id, UserModel.is_delete == 0)\
            .first()

    @classmethod
    def get_user_by_merchantid_username_and_password(cls, session, merchant_id, username, password):
        return session.query(UserModel)\
            .filter(UserModel.merchant_id == merchant_id, UserModel.username == username, UserModel.password == password, UserModel.is_delete != 1)\
            .first()

    @classmethod
    def get_users_by_merchant_id(cls, session, merchant_id):
        return session.query(UserModel)\
            .filter(UserModel.merchant_id == merchant_id, UserModel.is_delete != 1)\
            .first()

    @classmethod
    def update_user(cls, session, merchant_id, username, department, mobile, email, authority, is_valid):
        update_value = {}
        if department:
            update_value[UserModel.department] = department
        if mobile:
            update_value[UserModel.mobile] = mobile
        if email:
            update_value[UserModel.email] = email
        if authority:
            update_value[UserModel.authority] = authority
        if is_valid:
            update_value[UserModel.is_valid] = is_valid
        session.query(UserModel)\
            .filter(UserModel.merchant_id == merchant_id, UserModel.username == username, UserModel.is_delete == 0)\
            .update(update_value)
        session.commit()

    @classmethod
    def add_user(cls, session, merchant_id, username, password, re_password, department, mobile, email, authority):
        user = UserModel(merchant_id=merchant_id, username=username, password=password, department=department,
                         mobile=mobile, email=email, authority=authority)
        session.add(user)
        session.commit()
        return user

    def todict(self):
        return ObjectDict(
            id=self.id,
            merchant_id=self.merchant_id,
            username=self.username,
            nickname=self.nickname,
            department=self.department,
            mobile=self.mobile,
            email=self.email,
            authority=self.authority,
            is_delete=self.is_delete,
                )
