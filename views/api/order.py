# -*- coding: utf-8 -*-

from tornado.escape import json_encode, json_decode, url_escape
from tornado import gen

from tools.auth import auth_login
from tools.request_tools import get_and_valid_arguments
from views.base import BtwBaseHandler
from exception.json_exception import JsonException
from exception.celery_exception import CeleryException

from tasks.models import order as Order
from tasks.order import submit_order as SubmitOrder
from tasks.order import cancel_order as CancelOrder

class OrderWaitingAPIHandler(BtwBaseHandler):

    @gen.coroutine
    @auth_login(json=True)
    def get(self):
        merchant_id = self.current_user.merchant_id
        start = self.get_query_argument('start', 0)
        limit = self.get_query_argument('limit', 20)
        
        task = yield gen.Task(Order.get_waiting_orders.apply_async,
                args=[merchant_id, start, limit])
        print task.result
        if task.status == 'SUCCESS':
            orders, total = task.result
            self.finish_json(result={
                'orders': [order.todict() for order in orders],
                'total': total,
                'start': start,
                'limit': limit,
                })
        else:
            raise JsonException(errcode=1000, errmsg="wrong")


class OrderUserConfirmAPIHandler(BtwBaseHandler):

    @gen.coroutine
    @auth_login(json=True)
    def post(self, order_id):
        merchant_id = self.current_user.merchant_id

        task = yield gen.Task(SubmitOrder.confirm_order_by_user.apply_async,
                args=[merchant_id, order_id])
        if task.status == 'SUCCESS':
            self.finish_json(result=dict(
                order=task.result.todict(),
                ))
        else:
            if isinstance(task.result, CeleryException):
                raise JsonException(1000, task.result.errmsg)
            else:
                raise JsonException(1000, 'network error')

class OrderUserCancelAPIHandler(BtwBaseHandler):

    @gen.coroutine
    @auth_login(json=True)
    def post(self, order_id):
        merchant_id = self.current_user.merchant_id
        args = self.get_json_arguments()
        reason, = get_and_valid_arguments(args, 'reason')
        if not reason:
            raise JsonException(200, 'invalid reason')

        task = yield gen.Task(CancelOrder.cancel_order_by_user.apply_async,
                args=[merchant_id, order_id, reason])
        if task.status == 'SUCCESS':
            self.finish_json(result=dict(
                order=task.result.todict(),
                ))
        else:
            if isinstance(task.result, CeleryException):
                raise JsonException(1000, task.result.errmsg)
            else:
                raise JsonException(1000, 'network error')

class OrderTodayBookListAPIHandler(BtwBaseHandler):

    @gen.coroutine
    @auth_login(json=True)
    def get(self):
        merchant_id = self.current_user.merchant_id
        start = self.get_query_argument('start', 0)
        limit = self.get_query_argument('limit', 20)
        
        task = yield gen.Task(Order.get_today_book_orders.apply_async,
                args=[merchant_id, start, limit])
        print task.result
        if task.status == 'SUCCESS':
            orders, total = task.result
            self.finish_json(result={
                'total': total,
                'start': start,
                'limit': limit,
                'orders': [order.todict() for order in orders],
                })
        else:
            raise JsonException(errcode=1000, errmsg="wrong")

class OrderTodayCheckinListAPIHandler(BtwBaseHandler):

    @gen.coroutine
    @auth_login(json=True)
    def get(self):
        merchant_id = self.current_user.merchant_id
        start = self.get_query_argument('start', 0)
        limit = self.get_query_argument('limit', 20)
        
        task = yield gen.Task(Order.get_today_checkin_orders.apply_async,
                args=[merchant_id, start, limit])
        print task.result
        if task.status == 'SUCCESS':
            orders, total = task.result
            self.finish_json(result={
                'orders': [order.todict() for order in orders],
                'total': total,
                'start': start,
                'limit': limit,
                })
        else:
            raise JsonException(errcode=1000, errmsg="wrong")

class OrderSearchAPIHandler(BtwBaseHandler):

    @gen.coroutine
    @auth_login(json=True)
    def get(self):
        merchant_id = self.current_user.merchant_id

        args = self.get_json_arguments()
        
        order_id = args.get('order_id', None)
        hotel_name = args.get('hotel_name', None)
        checkin_date = args.get('checkin_date', None)
        checkout_date = args.get('checkout_date', None)
        customer = args.get('customer')
        order_status = args.get('order_status', None)
        create_time_start = args.get('create_time_start', None)
        create_time_end = args.get('create_time_end', None)





