# -*- coding -*-


from celery.schedules import crontab


CELERYBEAT_SCHEDULE = {
        'complete_inventory_in_four_months': {
            'task': 'tasks.models.inventory.test',
            'schedule': 5.0,
            'args': ('hello'),
            },
}
