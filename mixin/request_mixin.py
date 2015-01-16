# -*- coding: utf-8 -*-

from exception.celery_exception import CeleryException
from exception.json_exception import JsonException

class JsonRequestValidMixin(object):

    def prepare(self):
        self.request_json = self.get_request_json()


class CeleryTaskMixin(object):

    def process_celery_task(self, task, is_list=False):
        result = task.result
        if task.status == 'SUCCESS':
            if is_list:
                return result if result else []
            else:
                return result
        else:
            if isinstance(result, CeleryException):
                raise JsonException(errcode=result.errcode, errmsg=result.errmsg)
            else:
                raise JsonException(errcode=500, errmsg="server error")


