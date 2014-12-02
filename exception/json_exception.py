# -*- coding: utf-8 -*-

from tornado.escape import json_encode

class JsonException(Exception):
    '''
    json error 
    errcode start with 200
    '''

    def __init__(self, errcode, errmsg):
        self.errcode = errcode
        self.errmsg = errmsg

    def tojson(self):
        return json_encode({
            'errcode': self.errcode,
            'errmsg': self.errmsg,
            })


class JsonRequestTypeError(JsonException):

    def __init__(self, errcode="100", errmsg="need login", *args, **kwargs):
        super(JsonRequestTypeError, self).__init__(errcode, errmsg)

class JsonDecodeError(JsonException):

    def __init__(self, errcode="201", errmsg="wrong json arguments", *args, **kwargs):
        super(JsonDecodeError, self).__init__(errcode, errmsg)

class InvalidJsonArgumentError(JsonException):

    def __init__(self, errcode="202", errmsg="wrong json arguments", *args, **kwargs):
        super(InvalidJsonArgumentError, self).__init__(errcode, errmsg)


