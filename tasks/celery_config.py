# -*- coding -*-


from datetime import timedelta
from celery.schedules import crontab
import config

BROKER_URL = config.BROKER_URL
CELERY_RESULT_BACKEND = config.CELERY_RESULT_BACKEND
CELERY_ACCEPT_CONTENT = ['pickle']
BROKER_POOL_LIMIT = 100
CELERYD_PREFETCH_MULTIPLIER = 2
CELERY_IMPORTS = (
    'tasks.test', 'tasks.stock', 'tasks.poi',
                'tasks.models.cooperate_hotel', 'tasks.models.cooperate_roomtype',
                'tasks.models.inventory', 'tasks.models.rate_plan', 'tasks.models.room_rate',
                'tasks.models.order', 'tasks.models.user', 'tasks.models.merchant',
                'tasks.order.submit_order', 'tasks.order.submit_order_in_queue',
                'tasks.order.cancel_order', 'tasks.order.cancel_order_in_queue',)


CELERYBEAT_SCHEDULE = {
        'complete_inventory_in_four_months': {
            'task': 'tasks.models.inventory.complete_in_four_months',
            'schedule': crontab(hour=0, minute=0),
            },
        'push_all_to_poi': {
            'task': 'tasks.poi.push_poi',
            'schedule': crontab(hour=0, minute=0),
            },
}
