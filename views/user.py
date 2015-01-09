# -*- coding: utf-8 -*-

from tornado import gen
from base import BtwBaseHandler
from tornado.escape import json_encode
from tools.auth import auth_login, auth_permission
from constants import PERMISSIONS
from tasks.models.user import get_users_by_merchant_id

class UserManageHandler(BtwBaseHandler):

    @gen.coroutine
    @auth_login()
    @auth_permission(PERMISSIONS.admin)
    def get(self):
        task = yield gen.Task(get_users_by_merchant_id.apply_async,
                args=[self.current_user.merchant_id])
        if task.status == 'SUCCESS':
            users = task.result
            users = users if users else []
        else:
            users = []
        self.render("userManage.html", users=json_encode([user.todict() for user in users]))









