# -*- coding: utf-8 -*-

from tasks.celery_app import app
from tasks.base_task import SqlAlchemyTask
from constants import QUEUE_ORDER

from models.user import UserModel


@app.task(base=SqlAlchemyTask, bind=True)
def get_users_by_merchant_id(self, merchant_id):
    return UserModel.get_users_by_merchant_id(self.session, merchant_id)

@app.task(base=SqlAlchemyTask, bind=True)
def update_user(self, merchant_id, username, password, department, mobile, email, authority, is_valid):
    return UserModel.update_user(self.session, merchant_id, username, password, department, mobile, email, authority, is_valid)


@app.task(base=SqlAlchemyTask, bind=True)
def get_user_by_merchantid_username(self, merchant_id, username):
    return UserModel.get_user_by_merchantid_username(self.session, merchant_id, username)

@app.task(base=SqlAlchemyTask, bind=True)
def add_user(self, merchant_id, username, password, department, mobile, authority, is_valid):
    return UserModel.add_user(self.session, merchant_id, username, password, department, mobile, authority, is_valid)

@app.task(base=SqlAlchemyTask, bind=True)
def get_user_by_merchantid_username_and_password(self, merchant_id, username, password):
    return UserModel.get_user_by_merchantid_username_and_password(self.session, merchant_id, username, password)

@app.task(base=SqlAlchemyTask, bind=True)
def update_password(self, merchant_id, username, password):
        return UserModel.update_password(self.session, merchant_id, username, password)
