# -*- coding: utf-8 -*-

#from celery import current_app


from tasks.celery_app import app

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
