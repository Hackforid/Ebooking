# -*- coding: utf-8 -*-

import celery
from db import Session

class SqlAlchemyTask(celery.Task):

    abstract = True

    _session = None

    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        print 'after_return'
        self._session.remove()

    def on_failure(self, *args, **kwargs):
        print 'on_failure'

    @property
    def session(self):
        if self._session == None:
            print 'get db session'
            self._session = Session()
        return self._session

