# -*- coding: utf-8 -*-
import datetime

from tornado.util import ObjectDict 

from models import Base
from sqlalchemy import Column, DateTime
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
    valid_begin_date = Column('validBeginDate', DATETIME, nullable=False)
    valid_end_date = Column('validEndDate', DATETIME, nullable=False)
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
            .all()

    @classmethod
    def update_user(cls, session, merchant_id, username, password, department, mobile, email, authority, valid_begin_date,
                    valid_end_date, is_valid):
        user = cls.get_user_by_merchantid_username(session, merchant_id, username)
        if user:
            if password:
                user.password = password
            if department:
                user.department = department
            if mobile:
                user.mobile = mobile
            if email:
                user.email = email

            user.authority=authority
            user.valid_begin_date = valid_begin_date
            user.valid_end_date = valid_end_date
            user.is_valid = is_valid
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
            is_valid=self.is_valid,
            valid_begin_date=self.valid_begin_date.strftime('%Y-%m-%d'),
            valid_end_date=self.valid_end_date.strftime('%Y-%m-%d'),
            is_delete=self.is_delete,
                )
