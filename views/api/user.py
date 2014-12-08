# -*- coding: utf-8 -*-
import re

from views.base import BtwBaseHandler
from tools.auth import auth_login
from tools.auth import auth_permission
from models.user import UserModel
from constants import PERMISSIONS
from tornado.escape import json_encode
from tools.request_tools import get_and_valid_arguments

class UserManageAPIHandler(BtwBaseHandler):

    @auth_login()
    @auth_permission(PERMISSIONS.user_manage | PERMISSIONS.admin)
    def get(self):
        users = UserModel.get_users_by_merchant_id(self.db, self.current_user.merchant_id)
        return self.finish_json(0, u'成功', json_encode([user.todict() for user in users]))

    @auth_login(json=True)
    @auth_permission(PERMISSIONS.user_manage | PERMISSIONS.admin, json=True)
    def put(self):
        args = self.get_json_arguments()
        merchant_id, username, department, mobile, authority, is_valid = \
            get_and_valid_arguments(args, 'merchant_id', 'username', 'department', 'mobile', 'authority', 'is_valid')

        if args.has_key('email'):
            email = args['email']
        else:
            email = None

        if args.has_key('password'):
            password = args['password']
        else:
            password = None

        if password and ( len(password)<6 or len(password)>20 ):
            self.finish_json(1, u'请填写长度6-20位的正确密码')
            return

        if not self.mobile_check(mobile):
            self.finish_json(1, u'请填写正确手机号')
            return

        if not department:
            self.finish_json(1, u'请填写部门')
            return

        if self.current_user.merchant_id != merchant_id:
            self.finish_json(1, u'您只能管理自己的酒店')
            return

        ''' admin账号只能由admin自己修改 '''
        if (self.current_user.authority%2==0) and (authority%2==1):
            self.finish_json(1, u'您不能修改admin账户')
            return

        ''' admin 账号强制设定一些参数 '''
        if (self.current_user.authority%2==1):
            is_valid = 1

        ''' 可以管理用户 '''
        UserModel.update_user(self.db, merchant_id, username, password, department, mobile, email, authority, is_valid)

        ''' 修改了自己的密码 '''
        if self.current_user.username == username and password:
            self.clear_cookie('username')
            self.clear_cookie('merchant_id')
            self.finish_json(301, self.get_login_url())
            return

        self.finish_json(0, u'成功')

    @auth_login(json=True)
    @auth_permission(PERMISSIONS.user_manage | PERMISSIONS.admin, json=True)
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
        if authority%2==1:
            self.finish_json(1, u'不允许添加管理员用户')
            return
        if UserModel.get_user_by_merchantid_username(self.db, merchant_id, username):
            self.finish_json(1, u'用户名已被使用')
            return

        UserModel.add_user(session=self.db, merchant_id=merchant_id, username=username, password=password,
                           department=department, mobile=mobile, authority=authority, is_valid=is_valid)
        return self.finish_json(0, u'添加成功')

    @staticmethod
    def mobile_check(mobile):
        checker = re.compile(r"^1\d{10}$")
        if checker.match(mobile):
            return True
        return False
