# -*- coding -*-


from celery import Celery

from config import Config

app = Celery("celery_app",
        broker="amqp://admin:admin@localhost:5672/ebooking",
        backend ="amqp://admin:admin@localhost:5672/ebooking",
        include=['tasks.test', 'tasks.models.cooperate_hotel'],
        )


if __name__ == '__main__':
    app.start()
