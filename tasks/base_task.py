# -*- coding: utf-8 -*-

#from gevent import monkey
#monkey.patch_all()

import celery
from celery.utils.log import get_task_logger
from tasks.db import Session

class SqlAlchemyTask(celery.Task):

    abstract = True

    _session = None

    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        self._session.remove()

    def on_failure(self, *args, **kwargs):
        print 'on_failure'

    @property
    def session(self):
        if self._session == None:
            self._session = Session
        return self._session

    @property
    def log(self):
        return get_task_logger('%s.%s' % (__name__, self.__class__.__name__))

