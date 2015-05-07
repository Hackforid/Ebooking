# -*- coding: utf-8 -*-

from tornado.escape import json_encode, json_decode, url_escape
from tornado import gen

from exception.json_exception import JsonException

from tools.auth import auth_backstage_login, need_backstage_admin
from tools.request_tools import get_and_valid_arguments
from views.base import BackStageHandler
from models.merchant import MerchantModel
from models.user import UserModel
from models.cooperate_hotel import CooperateHotelModel


from tasks.stock import PushHotelTask

class AdminMerchantAPIHandler(BackStageHandler):

    @auth_backstage_login(json=True)
    @need_backstage_admin(json=True)
    def get(self):
        merchants = MerchantModel.get_all(self.db)
        merchants = [merchant.todict() for merchant in merchants]
        self.finish_json(result=dict(
            merchants=merchants
            ))

class AdminMerchantModifyAPIHandler(BackStageHandler):

    @auth_backstage_login(json=True)
    @need_backstage_admin(json=True)
    def post(self):
        args = self.get_json_arguments()
        merchant, root_pwd, admin_pwd = get_and_valid_arguments(args, 'merchant', 'root_pwd', 'admin_pwd')
        name, type = get_and_valid_arguments(merchant, 'name', 'type')

        merchant, admin, root = self.new_merchant(name, type, admin_pwd, root_pwd)

        self.finish_json(result=dict(
            merchant=merchant.todict(),
            admin=admin.todict(),
            root=root.todict(),
            ))

    def new_merchant(self, name, type, admin_pwd, root_pwd):
        merchant = MerchantModel.new_merchant(self.db, name, type)
        admin, root = UserModel.new_admin_root_user(self.db, merchant.id, admin_pwd, root_pwd)
        return merchant, admin, root


    @auth_backstage_login(json=True)
    @need_backstage_admin(json=True)
    def put(self):
        args = self.get_json_arguments()
        merchant, = get_and_valid_arguments(args, 'merchant')
        id, name, type = get_and_valid_arguments(merchant, 'id', 'name', 'type')

        admin_pwd = args.get('admin_pwd', None)
        root_pwd = args.get('root_pwd', None)

        merchant = self.modify_merchant(id, name, type, admin_pwd, root_pwd)

        self.finish_json(result=dict(
            merchant=merchant.todict(),
            ))

    def modify_merchant(self, id, name, type, admin_pwd, root_pwd):
        merchant = MerchantModel.get_by_id(self.db, id)
        if not merchant:
            raise JsonException(errcode=404, errmsg="merchant not fount")
        else:
            merchant.update(self.db, name, type)

        if admin_pwd:
            UserModel.update_password(self.db, merchant.id, 'admin', admin_pwd)
        if root_pwd:
            UserModel.update_password(self.db, merchant.id, 'root', root_pwd)

        return merchant

class AdminMerchantSuspendAPIHandler(BackStageHandler):


    @auth_backstage_login(json=True)
    @need_backstage_admin(json=True)
    def put(self, merchant_id, is_suspend):

        merchant = self.suspend_merchant(merchant_id, is_suspend)
        self.finish_json(result=dict(
            merchant=merchant.todict(),
            ))

    def suspend_merchant(self, merchant_id, is_suspend):
        is_suspend = int(is_suspend)
        merchant = MerchantModel.get_by_id(self.db, merchant_id)
        if not merchant:
            raise JsonException(errcode=404, errmsg="merchant not fount")

        merchant.is_suspend = is_suspend
        CooperateHotelModel.set_suspend_by_merchant_id(self.db, merchant_id, is_suspend)

        self.db.commit()

        PushHotelTask().push_hotel_suspend_by_merchant_id.delay(merchant_id)
        return merchant

