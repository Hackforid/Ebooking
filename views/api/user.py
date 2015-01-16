# -*- coding: utf-8 -*-
import re

from tornado.escape import json_encode
from tornado import gen


from views.base import BtwBaseHandler
from tools.auth import auth_login
from tools.auth import auth_permission
from constants import PERMISSIONS
from tools.request_tools import get_and_valid_arguments

from tasks.models import user as User

class UserManageAPIHandler(BtwBaseHandler):

    @gen.coroutine
    @auth_login()
    @auth_permission(PERMISSIONS.admin)
    def get(self):
        task = yield gen.Task(User.get_users_by_merchant_id.apply_async,
                args=[self.current_user.merchant_id])
        users = task.result
        self.finish_json(0, u'成功', json_encode([user.todict() for user in users]))

    @gen.coroutine
    @auth_login(json=True)
    @auth_permission(PERMISSIONS.admin, json=True)
    def put(self):
        args = self.get_json_arguments()
        merchant_id, username, department, mobile, authority, is_valid = \
            get_and_valid_arguments(args, 'merchant_id', 'username', 'department', 'mobile', 'authority', 'is_valid')

        if 'email' in args:
            email = args['email']
        else:
            email = None

        if 'password' in args:
            password = args['password']
        else:
            password = None

        if not self.mobile_check(mobile):
            self.finish_json(1, u'请填写正确手机号')
            return

        if not department:
            self.finish_json(1, u'请填写部门')
            return

        if self.current_user.merchant_id != merchant_id:
            self.finish_json(1, u'您只能管理自己的酒店')
            return

        ''' 可以管理用户 '''
        yield gen.Task(User.update_user.apply_async,
                args=[merchant_id, username, password, department, mobile, email, authority, is_valid])



        ''' 修改了自己的密码 '''
        if self.current_user.username == username and password:
            self.clear_cookie('username')
            self.clear_cookie('merchant_id')
            self.finish_json(301, self.get_login_url())
            return

        self.finish_json(0, u'成功')

    @gen.coroutine
    @auth_login(json=True)
    @auth_permission(PERMISSIONS.admin, json=True)
    def post(self):
        args = self.get_json_arguments()
        merchant_id, username, password, re_password, department, mobile, authority, is_valid = \
            get_and_valid_arguments(args, 'merchant_id', 'username', 'password', 're_password', 'department', 'mobile',
                                    'authority', 'is_valid')

        if merchant_id != self.current_user.merchant_id:
            self.finish_json(1, u'您只能管理自己的酒店')
            return
        if not username:
            self.finish_json(1, u'请填写用户名')
            return
        if (not password) or (not re_password):
            self.finish_json(1, u'请输入密码')
            return
        if password != re_password:
            self.finish_json(1, u'两次密码不一致')
            return
        if not department:
            self.finish_json(1, u'请输入部门')
            return
        if not mobile:
            self.finish_json(1, u'请输入手机号')
            return
        if authority & PERMISSIONS.admin or authority & PERMISSIONS.root:
            self.finish_json(1, u'不允许添加管理员用户')
            return

        user = (yield gen.Task(User.get_user_by_merchantid_username.apply_async, args=[merchant_id, username])).result

        if user:
            self.finish_json(1, u'用户名已被使用')
        else:
            yield gen.Task(User.add_user.apply_async,
                    args=[merchant_id, username, password, department, mobile, authority, is_valid])
            self.finish_json(0, u'添加成功')

    @staticmethod
    def mobile_check(mobile):
        checker = re.compile(r"^1\d{10}$")
        if checker.match(mobile):
            return True
        return False
