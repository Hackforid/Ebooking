# -*- coding: utf-8 -*-

import celery
from sqlalchemy.orm import scoped_session
from db import db_session

class SqlAlchemyTask(celery.Task):

    abstract = True

    _session = None

    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        self.session.remove()

    @property
    def session(self):
        if self._session is None:
            self._session = scoped_session(db_session)

        return self._session

