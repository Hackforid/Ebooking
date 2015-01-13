# -*- coding: utf-8 -*-

from tornado.util import ObjectDict 

from models import Base
from sqlalchemy import Column, DateTime
from sqlalchemy.dialects.mysql import BIT, INTEGER, VARCHAR, DATETIME, BIGINT
from tools.auth import md5_password


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
        password = md5_password(password)
        return session.query(UserModel)\
            .filter(UserModel.merchant_id == merchant_id, UserModel.username == username, UserModel.password == password,
                    UserModel.is_delete == 0, UserModel.is_valid == 1)\
            .first()

    @classmethod
    def get_users_by_merchant_id(cls, session, merchant_id):
        return session.query(UserModel)\
            .filter(UserModel.merchant_id == merchant_id, UserModel.is_delete == 0)\
            .all()

    @classmethod
    def update_user(cls, session, merchant_id, username, password, department, mobile, email, authority, is_valid):
        if password:
            password = md5_password(password)
        user = cls.get_user_by_merchantid_username(session, merchant_id, username)
        if user:
            if password:
                user.password = password
            user.department = department
            user.mobile = mobile
            if email:
                user.email = email
            user.authority=authority
            user.is_valid = is_valid
            session.commit()

    @classmethod
    def update_password(cls, session, merchant_id, username, password):
        password = md5_password(password)
        user = cls.get_user_by_merchantid_username(session, merchant_id, username)
        if user:
            user.password = password
            session.commit()

    @classmethod
    def add_user(cls, session, merchant_id, username, password, department, mobile, authority, is_valid):
        password = md5_password(password)
        user = UserModel(merchant_id=merchant_id, username=username, nickname='', password=password, department=department,
                         mobile=mobile, email='', authority=authority, is_valid=is_valid)
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
            is_delete=self.is_delete,
                )
