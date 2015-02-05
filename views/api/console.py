# -*- coding: utf-8 -*-

from constants import PERMISSIONS
from tools.auth import auth_login, auth_permission
from views.base import BtwBaseHandler

from tasks.poi import POIPushTask
from tasks.stock import push_all_to_stock 


class POIPushAllAPIHandler(BtwBaseHandler):

    @auth_login(json=True)
    @auth_permission(PERMISSIONS.admin, json=True)
    def get(self):
        POIPushTask().push_all.delay()
        self.finish_json(errcode=0, result=[])


class StockPushAllAPIHandler(BtwBaseHandler):

    @auth_login(json=True)
    @auth_permission(PERMISSIONS.admin, json=True)
    def get(self):
        push_all_to_stock.delay()
        self.finish_json(errcode=0, result=[])
