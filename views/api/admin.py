# -*- coding: utf-8 -*-

from tornado.escape import json_encode, json_decode, url_escape
from tornado import gen

from tools.auth import auth_login, auth_permission, need_btw_admin
from tools.request_tools import get_and_valid_arguments
from views.base import BtwBaseHandler
import tasks.models.cooperate_hotel as CooperateHotel
import tasks.models.merchant as Merchant

from exception.json_exception import JsonException
from exception.celery_exception import CeleryException
from constants import PERMISSIONS

from mixin.request_mixin import CeleryTaskMixin

class AdminMerchantAPIHandler(BtwBaseHandler, CeleryTaskMixin):

    @gen.coroutine
    @auth_login(json=True)
    @need_btw_admin(json=True)
    def get(self):

        task = yield gen.Task(Merchant.get_merchant_list.apply_async)
        merchants = self.process_celery_task(task, is_list=True)
        
        merchants = [merchant.todict() for merchant in merchants]
        self.finish_json(result=dict(
            merchants=merchants
            ))

class AdminMerchantModifyAPIHandler(BtwBaseHandler, CeleryTaskMixin):

    @gen.coroutine
    @auth_login(json=True)
    @need_btw_admin(json=True)
    def post(self):
        args = self.get_json_arguments()
        merchant, root_pwd, admin_pwd = get_and_valid_arguments(args, 'merchant', 'root_pwd', 'admin_pwd')
        
        name, type = get_and_valid_arguments(merchant, 'name', 'type')

        task = yield gen.Task(Merchant.new_merchant.apply_async,
                args=[name, type, admin_pwd, root_pwd])

        merchant, admin, root = self.process_celery_task(task)
        self.finish_json(result=dict(
            merchant=merchant.todict(),
            admin=admin.todict(),
            root=root.todict(),
            ))

    @gen.coroutine
    @auth_login(json=True)
    @need_btw_admin(json=True)
    def put(self):
        args = self.get_json_arguments()
        merchant, = get_and_valid_arguments(args, 'merchant')
        id, name, type = get_and_valid_arguments(merchant, 'id', 'name', 'type')

        admin_pwd = args.get('admin_pwd', None)
        root_pwd = args.get('root_pwd', None)

        task = yield gen.Task(Merchant.modify_merchant.apply_async,
                args=[id, name, type, admin_pwd, root_pwd])

        merchant = self.process_celery_task(task)
        self.finish_json(result=dict(
            merchant=merchant.todict(),
            ))

class AdminMerchantSuspendAPIHandler(BtwBaseHandler, CeleryTaskMixin):


    @gen.coroutine
    @auth_login(json=True)
    #@need_btw_admin(json=True)
    def put(self, merchant_id, is_suspend):

        task = yield gen.Task(Merchant.suspend_merchant.apply_async,
                args=[merchant_id, is_suspend])

        merchant = self.process_celery_task(task)
        self.finish_json(result=dict(
            merchant=merchant.todict(),
            ))
