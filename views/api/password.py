# -*- coding: utf-8 -*-

from tornado import gen

from views.base import BtwBaseHandler
from tools.auth import auth_login, auth_permission, md5_password
from tools.request_tools import get_and_valid_arguments
from constants import PERMISSIONS
from tasks.models.user import update_password

class PasswordAPIHandler(BtwBaseHandler):

    @gen.coroutine
    @auth_login(json=True)
    @auth_permission(PERMISSIONS.update_password, json=True)
    def put(self):
        print '==' * 20
        args = self.get_json_arguments()
        print args
        old_password, password, re_password = get_and_valid_arguments(args, 'old_password', 'password', 're_password')

        old_password = md5_password(old_password)
        if self.current_user.password != old_password:
            print u'密码不对'
            print self.current_user.password, old_password
            self.finish_json(1, u'旧密码不正确')
            return

        if (not password) or (not re_password):
            print u'请输入正确密码'
            self.finish_json(1, u'请输入正确密码')
            return

        if password != re_password:
            print u'两次密码不一致'
            self.finish_json(1, u'两次密码不一致')
            return

        if md5_password(password) == self.current_user.password:
            print u'新密码和旧密码相同'
            self.finish_json(1, u'新密码和旧密码相同')
            return

        task = yield gen.Task(update_password.apply_async,
                args=[self.current_user.merchant_id, self.current_user.username, password])

        if task.status == 'SUCCESS':
            self.clear_cookie('username')
            self.clear_cookie('merchant_id')
            self.finish_json(0, '修改成功')
        else:
            self.finish_json(1000, 'error')
