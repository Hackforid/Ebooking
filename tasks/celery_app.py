# -*- coding -*-


from celery import Celery

from config import Config

app = Celery("celery_app",
        broker="amqp://admin:admin@localhost:5672/ebooking",
        backend ="amqp://admin:admin@localhost:5672/ebooking",
        include=['tasks.test', 'tasks.models.cooperate_hotel', 'tasks.models.cooperate_roomtype',
            'tasks.models.inventory', 'tasks.models.rate_plan', 'tasks.models.room_rate',
            'tasks.order.submit_order', 'tasks.order.submit_order_in_queue'],
        )


if __name__ == '__main__':
    app.start()
