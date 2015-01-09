# -*- coding: utf-8 -*-

import hashlib
from config import PASSWORD_SALT


def auth_login(json=False):
    def _decorator(fn):
        def _(self, *args, **kwargs):

            if self.current_user:
                return fn(self, *args, **kwargs)
            else:
                if json:
                    self.finish_json(errcode=100, errmsg="need login")
                else:
                    self.redirect(self.get_login_url())
        return _
    return _decorator


def auth_permission(permissions, json=False):
    def _decorator(fn):
        def _(self, *args, **kwargs):

            if self.current_user.authority & permissions:
                return fn(self, *args, **kwargs)
            else:
                if json:
                    self.finish_json(errcode=401, errmsg="permission denied")
                else:
                    self.redirect(self.get_login_url())
        return _
    return _decorator

def md5_password(password):
    pwd = "{}|{}".format(password, PASSWORD_SALT)
    m = hashlib.md5()
    m.update(pwd)
    return m.hexdigest()


