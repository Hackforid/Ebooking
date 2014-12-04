# -*- coding: utf-8 -*-

from base import BtwBaseHandler
from models.user import UserModel
from tornado.escape import json_encode
from tools.auth import auth_login
from tools.auth import auth_permission
from constants import PERMISSIONS
from tools.request_tools import get_and_valid_arguments
from exception.json_exception import JsonException

class UserManageHandler(BtwBaseHandler):


    @auth_login()
    @auth_permission(PERMISSIONS.user_manage | PERMISSIONS.admin)
    def get(self):
        users = UserModel.get_users_by_merchant_id(self.db, self.current_user.merchant_id)
        return self.render("userManage.html", users=json_encode([user.todict() for user in users]))

    @auth_login()
    @auth_permission(PERMISSIONS.user_manage | PERMISSIONS.admin, json=True)
    def put(self):
        args = self.get_json_arguments()
        merchant_id, username, authority, valid_begin_date, valid_end_date, is_valid \
            = get_and_valid_arguments(args, 'merchant_id', 'username', 'authority', 'valid_begin_date',
                                      'valid_end_date', 'is_valid')

        if args.has_key('department'):
            department = args['department']
        else:
            department = None
        if args.has_key('mobile'):
            mobile = args['mobile']
        else:
            mobile = None
        if args.has_key('email'):
            email = args['email']
        else:
            email = None
        if args.has_key('password'):
            password = args['password']
        else:
            password = None

        if self.current_user.merchant_id != merchant_id:
            self.finish_json(1, u'您只能管理自己的酒店')
            return

        ''' admin账号只能由admin自己修改 '''
        if (self.current_user.authority==0) and (authority%2==1):
            self.finish_json(1, u'您不能修改')
            return

        ''' admin 账号强制设定一些参数 '''
        if (self.current_user.authority%2==1):
            is_valid = 1
            valid_begin_date = '2014-01-01'
            valid_end_date = '2999-12-21'

        ''' 可以管理用户 '''
        UserModel.update_user(self.db, merchant_id, username, password, department, mobile, email, authority,
                              valid_begin_date, valid_end_date, is_valid)

        ''' 修改了自己的密码 '''
        if self.current_user.username == username and password:
            self.clear_cookie('username')
            self.clear_cookie('merchant_id')
            self.finish_json(301, self.get_login_url())
            return

        self.finish_json(0, u'成功')





