# -*- coding: utf-8 -*-


from tasks.celery_app import app
from tasks.base_task import SqlAlchemyTask
from tasks.stock import PushRatePlanTask

from models.merchant import MerchantModel
from models.user import UserModel
from exception.celery_exception import CeleryException


@app.task(base=SqlAlchemyTask, bind=True)
def get_merchant_list(self):
    return MerchantModel.get_all(self.session)

@app.task(base=SqlAlchemyTask, bind=True)
def new_merchant(self, name, type, admin_pwd, root_pwd):
    merchant = MerchantModel.new_merchant(self.session, name, type)
    admin, root = UserModel.new_admin_root_user(self.session, merchant.id, admin_pwd, root_pwd)
    return merchant, admin, root


@app.task(base=SqlAlchemyTask, bind=True)
def modify_merchant(self, id, name, type, admin_pwd, root_pwd):
    merchant = MerchantModel.get_by_id(self.session, id)
    if not merchant:
        raise CeleryException(errcode=404, errmsg="merchant not fount")
    else:
        merchant.update(self.session, name, type)

    if admin_pwd:
        UserModel.update_password(self.session, merchant.id, 'admin', admin_pwd)
    if root_pwd:
        UserModel.update_password(self.session, merchant.id, 'root', root_pwd)

    return merchant



