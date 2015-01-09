# -*- coding: utf-8 -*-

import requests
import json


from tasks.celery_app import app
from tasks.base_task import SqlAlchemyTask

from exception.celery_exception import CeleryException
from tools.json import json_encode


@app.task(base=SqlAlchemyTask, bind=True, ignore_result=True)
def send_sms(phones, content):
    if not content:
        return

    url = "http://10.200.11.119:8090/member/send_sms"

    for phone in phones:
        obj = {}
        obj['mobile'] = phone
        obj['content'] = content
        r = requests.post(url, json=obj)
