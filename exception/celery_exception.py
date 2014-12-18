# -*- coding: utf-8 -*-


class CeleryException(object):

    def __init__(self, errcode, errmsg):
        self.errcode = errcode
        self.errmsg = errmsg

