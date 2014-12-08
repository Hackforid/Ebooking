# -*- coding: utf-8 -*-
from views.base import BtwBaseHandler
from tools.auth import auth_login
from tools.request_tools import get_and_valid_arguments
from models.user import UserModel

class PasswordAPIHandler(BtwBaseHandler):

    @auth_login(json=True)
    def put(self):
        args = self.get_json_arguments()
        old_password, password, re_password = get_and_valid_arguments(args, 'old_password', 'password', 're_password')

        if self.current_user.password != old_password:
            self.finish_json(1, u'旧密码不正确')
            return

        if (not password) or (not re_password):
            self.finish_json(1, u'请输入正确密码')
            return

        if password != re_password:
            self.finish_json(1, u'两次密码不一致')
            return

        if password == self.current_user.password:
            self.finish_json(1, u'新密码和旧密码相同')
            return

        UserModel.update_password(self.db, self.current_user.merchant_id, self.current_user.username, password)
        self.clear_cookie('username')
        self.clear_cookie('merchant_id')
        self.finish_json(0, '修改成功')
