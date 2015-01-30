# -*- coding: utf-8 -*-

#from celery import current_app


from tasks.celery_app import app
from tasks.base_task import SqlAlchemyTask
from models.merchant import MerchantModel
from exception.celery_exception import CeleryException

@app.task
def tt(num):
    import time
    for i in range(10):
        print i
        time.sleep(1)
    return num + 3

class Test(object):

    @classmethod
    @app.task
    def plus(num):
        import time
        for i in range(10):
            print i
            time.sleep(1)
        return num + 3

@app.task(base=SqlAlchemyTask, bind=True, ignore_result=True)
def helloworld(self):
    print 'helloworld'
    merchants = MerchantModel.get_all(self.session)
    raise CeleryException(errcode=100, errmsg='he')

    return merchants
