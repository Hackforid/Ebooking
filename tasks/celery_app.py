# -*- coding -*-


from celery import Celery

from config import Config

app = Celery("celery_app",
        broker="amqp://admin:admin@localhost:5672/ebooking",
        backend ="amqp://admin:admin@localhost:5672/ebooking",
        include=['tasks.test', 'tasks.stock',
            'tasks.models.cooperate_hotel', 'tasks.models.cooperate_roomtype',
            'tasks.models.inventory', 'tasks.models.rate_plan', 'tasks.models.room_rate',
            'tasks.models.order', 'tasks.models.user',
            'tasks.order.submit_order', 'tasks.order.submit_order_in_queue',
            'tasks.order.cancel_order', 'tasks.order.cancel_order_in_queue'],
        )


if __name__ == '__main__':
    app.start()
