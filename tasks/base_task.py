# -*- coding: utf-8 -*-

import celery
from sqlalchemy.orm import scoped_session
from db import db_session

class SqlAlchemyTask(celery.Task):

    abstract = True

    _session = None

    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        print 'after_return'
        db_session.remove()

    def on_failure(self, *args, **kwargs):
        print 'on_failure'

    @property
    def session(self):
        print 'get db session'
        return db_session

