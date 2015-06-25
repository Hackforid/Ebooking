# -*- coding: utf-8 -*-

import hashlib
from config import PASSWORD_SALT, BACKSTAGE_PERMISSIONS, BACKSTAGE_ENABLE


def auth_login(json=False):
    def _decorator(fn):
        def _(self, *args, **kwargs):

            if self.current_user and (self.merchant.id == 1 or self.merchant.is_suspend == 0):
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



def no_monomer_hotel(json=False):
    def _decorator(fn):
        def _(self, *args, **kwargs):

            if self.merchant.type != self.merchant.TYPE_MONOMER_HOTEL or self.current_user.type == self.current_user.TYPE_ROOT:
                return fn(self, *args, **kwargs)
            else:
                if json:
                    self.finish_json(errcode=100, errmsg="no permission")
                else:
                    self.redirect(self.get_login_url())
        return _
    return _decorator

def need_btw_admin(json=False):
    def _decorator(fn):
        def _(self, *args, **kwargs):

            if self.merchant.id == 1:
                return fn(self, *args, **kwargs)
            else:
                if json:
                    self.finish_json(errcode=100, errmsg="no permission")
                else:
                    self.redirect(self.get_login_url())
        return _
    return _decorator

def auth_backstage_login(json=False):
    def _decorator(fn):
        def _(self, *args, **kwargs):

            if self.backstage_user_name or not BACKSTAGE_ENABLE:
                return fn(self, *args, **kwargs)
            else:
                if json:
                    self.finish_json(errcode=100, errmsg="need backstage login")
                else:
                    self.finish('need backstage login')
        return _
    return _decorator

def need_backstage_admin(json=False):
    def _decorator(fn):
        def _(self, *args, **kwargs):

            if BACKSTAGE_PERMISSIONS['admin'] in self.backstage_user_permissions or not BACKSTAGE_ENABLE:
                return fn(self, *args, **kwargs)
            else:
                if json:
                    self.finish_json(errcode=401, errmsg="permission denied")
                else:
                    self.finish('permission denied')
        return _
    return _decorator

def need_backstage_ota(json=False):
    def _decorator(fn):
        def _(self, *args, **kwargs):

            if BACKSTAGE_PERMISSIONS['ota'] in self.backstage_user_permissions or not BACKSTAGE_ENABLE:
                return fn(self, *args, **kwargs)
            else:
                if json:
                    self.finish_json(errcode=401, errmsg="permission denied")
                else:
                    self.finish('permission denied')
        return _
    return _decorator
