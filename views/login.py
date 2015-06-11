# -*- coding: utf-8 -*-


from views.base import BtwBaseHandler
from views import BaseHandler

from tools.auth import auth_login
from tools.request_tools import get_and_valid_arguments
from models.user import UserModel

from tools.request_tools import clear_domain_cookie

class LoginHandler(BtwBaseHandler):

    def get(self):
        self.render("index.html")

    def post(self):
        args = self.get_json_arguments()

        merchant_id, username, password = get_and_valid_arguments(args,
                'merchant_id', 'username', 'password')

        user = UserModel.get_user_by_merchantid_username_and_password(self.db, merchant_id, username, password)

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
        clear_domain_cookie(self, "open_id", domain=".betterwood.com")
        clear_domain_cookie(self, "username", domain=".betterwood.com")
        clear_domain_cookie(self, "merchant_id", domain=".betterwood.com")
        clear_domain_cookie(self, "open_id")
        clear_domain_cookie(self, "username")
        clear_domain_cookie(self, "merchant_id")
        self.redirect("/login/")
