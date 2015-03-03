# -*- coding: utf-8 -*-

from __future__ import absolute_import

import requests

from models.user import UserModel
from models.order import OrderModel

from tasks.celery_app import app
from tasks.base_task import SqlAlchemyTask

from tools.log import Log
from config import ORDER_CONTACTS

@app.task(base=SqlAlchemyTask, bind=True, ignore_result=True)
def send_order_sms(self, merchant_id, hotel_name, order_id, confirm_type):
    Log.info(u">>> send sms to merchant {} hotel {} order_id {} confirm type {}".format(merchant_id, hotel_name, order_id, confirm_type))
    user =UserModel.get_user_by_merchantid_username(self.session, merchant_id, 'admin')
    if not user:
        Log.info("send sms no user(order {})".format(order_id))
        return
    phone = user.mobile
    if not phone:
        Log.info("send sms no phone(order {})".format(order_id))
        return
    if confirm_type == OrderModel.CONFIRM_TYPE_AUTO:
        content = u"【商旅分销管理系统】尊敬的用户您好，系统收到了[{}]的自动确认订单，订单号:{}，请予以关注。".format(hotel_name, order_id)
    elif confirm_type == OrderModel.CONFIRM_TYPE_MANUAL:
        content = u"【商旅分销管理系统】尊敬的用户您好，系统收到了[{}]的待确认订单，订单号:{}，请尽快处理。".format(hotel_name, order_id)

    Log.info(">> send sms to {}".format(phone))
    Log.info(u">> sms content: {}".format(content))
    
    send_sms([phone], content)
    send_sms_to_service(merchant_id, content)


def send_sms(phones, content):
    if not content:
        return

    url = "http://10.200.11.119:8090/member/send_sms"

    for phone in phones:
        obj = {}
        obj['mobile'] = phone
        obj['content'] = content
        r = requests.post(url, json=obj)
        Log.info(">> send sms resp {}".format(r.text))


def send_sms_to_service(merchant_id, content):
    content = u"merchant {} 收到新订单: {}".format(merchant_id, content)
    send_sms(ORDER_CONTACTS, content)
