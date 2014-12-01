# -*- coding: utf-8 -*-

from tornado.escape import json_encode

from views import BaseHandler

class BtwBaseHandler(BaseHandler):

    def _handle_request_exception(self, e):
        super(BtwBaseHandler, self)._handle_request_exception(e)

    def finish_json(self, errcode=0, errmsg=None, result=None):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        self.finish(json_encode({'errcode': errcode,
                    'errmsg': errmsg,
                    'result': result}))
