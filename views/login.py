# -*- coding: utf-8 -*-

from tornado import gen

from views.base import BtwBaseHandler
from views import BaseHandler
from tasks.models.user import get_user_by_merchantid_username_and_password

from tools.auth import auth_login
from tools.request_tools import get_and_valid_arguments

class LoginHandler(BtwBaseHandler):

    def get(self):
        self.render("index.html")

    @gen.coroutine
    def post(self):
        args = self.get_json_arguments()
        print "<<user login>> {}".format(args)

        merchant_id, username, password = get_and_valid_arguments(args,
                'merchant_id', 'username', 'password')

        user = (yield gen.Task(get_user_by_merchantid_username_and_password.apply_async,
                args=[merchant_id, username, password])).result

        if user:
            self.set_secure_cookie("username", user.username, expires_days=0.02)
            self.set_secure_cookie("merchant_id", str(user.merchant_id), expires_days=0.02)
            self.finish_json(result={
                'user':user.todict()
                })
        else:
            self.finish_json(errcode=100, errmsg=u"帐号或密码错误")

class LogoutHandler(BtwBaseHandler):

    @auth_login()
    def get(self):
        self.clear_all_cookies()
        self.redirect("/login/")
