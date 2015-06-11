# -*- coding: utf-8 -*-


class CeleryException(Exception):

    def __init__(self, errcode, errmsg):
        self.errcode = errcode
        self.errmsg = errmsg
        super(Exception, self).__init__(errcode, errmsg)
