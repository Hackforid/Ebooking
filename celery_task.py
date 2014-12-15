# -*- coding -*-

from celery import Celery


app = Celery("celery_task",
        broker="amqp://admin:admin@localhost:5672/ebooking",
        backend ="amqp://admin:admin@localhost:5672/ebooking",
        )

@app.task
def show(num):
    import time
    for i in range(10):
        print i
        time.sleep(1)
    return num + 3

if __name__ == '__main__':
    app.start()

