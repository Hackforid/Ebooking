# -*- coding: utf-8 -*-

#from gevent import monkey
#monkey.patch_all()

import celery
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

