# -*- coding -*-

from celery import Celery

from config import Config

app = Celery("celery_app")

app.config_from_object('tasks.celery_config')

if __name__ == '__main__':
    app.start()
