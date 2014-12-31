# -*- coding -*-


from datetime import timedelta
from celery.schedules import crontab

BROKER_URL = "amqp://admin:admin@localhost:5672/ebooking"
CELERY_RESULT_BACKEND = "amqp://admin:admin@localhost:5672/ebooking"
CELERY_IMPORTS = (
    'tasks.test', 'tasks.stock',
                'tasks.models.cooperate_hotel', 'tasks.models.cooperate_roomtype',
                'tasks.models.inventory', 'tasks.models.rate_plan', 'tasks.models.room_rate',
                'tasks.models.order', 'tasks.models.user',
                'tasks.order.submit_order', 'tasks.order.submit_order_in_queue',
                'tasks.order.cancel_order', 'tasks.order.cancel_order_in_queue',)


CELERYBEAT_SCHEDULE = {
        'complete_inventory_in_four_months': {
            'task': 'tasks.models.inventory.complete_in_four_months',
            'schedule': crontab(hour=0, minute=0),
            },
}
