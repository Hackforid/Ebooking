# -*- coding: utf-8 -*-

import celery
from celery.utils.log import get_task_logger
from tasks.db import Session
from tools.log import Log

class SqlAlchemyTask(celery.Task):

    abstract = True

    _session = None

    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        Log.info('after_return')
        Session.remove()
        Log.info('remove session')

    def on_failure(self, exception, *args, **kwargs):
        Log.info('on_failure')
        Session.rollback()
        Session.remove()
        Log.info('rollback and remove session')

    @property
    def session(self):
        if self._session == None:
            self._session = Session()
        return self._session

    @property
    def log(self):
        return get_task_logger('%s.%s' % (__name__, self.__class__.__name__))

class OrderTask(SqlAlchemyTask):

    def log_order(self):
        pass
