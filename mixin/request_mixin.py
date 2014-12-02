# -*- coding: utf-8 -*-

class JsonRequestValidMixin(object):

    def prepare(self):
        self.request_json = self.get_request_json()


