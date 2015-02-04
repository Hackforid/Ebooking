# -*- coding: utf-8 -*-

from datetime import date

from tornado import gen
from tornado.httpclient import AsyncHTTPClient
from tornado.escape import json_encode, json_decode

from config import API
from views.base import BtwBaseHandler
from models.order import OrderModel
from models.income import IncomeModel
from tools.auth import auth_login, auth_permission
from tools.request_tools import get_and_valid_arguments
from constants import PERMISSIONS, OTA
from exception.json_exception import JsonException


class FinanceAPIHandler(BtwBaseHandler):

    @auth_login(json=True)
    @auth_permission(PERMISSIONS.admin | PERMISSIONS.income_statistics, json=True)
    def get(self):
        today = date.today()
        year = int(self.get_query_argument('year', today.year))
        month = int(self.get_query_argument('month', today.month))
        ota_id = self.get_query_argument('ota_id', None)
        pay_type = int(self.get_query_argument('pay_type', 1))
        merchant_id =self.current_user.merchant_id

        orders = self.get_order_in_date(merchant_id, year, month, pay_type, ota_id)
        incomes = self.get_income_record_in_date(merchant_id, year, month, pay_type, ota_id)

        self.finish_json(result=dict(
            orders=[order.todict() for order in orders],
            incomes=[income.todict() for income in incomes],
            ))


    def get_order_in_date(self, merchant_id, year, month, pay_type, ota_id=None):
        orders = OrderModel.get_success_order_by_checkout_date_in_month(self.db,
                merchant_id, year, month, pay_type, ota_id)
        return orders

    def get_income_record_in_date(self, merchant_id, year, month, pay_type, ota_id=None):
        incomes = IncomeModel.get_in_month(self.db, merchant_id, year, month, pay_type, ota_id)
        return incomes


class IncomeAPIHandler(BtwBaseHandler):

    @auth_login(json=True)
    @auth_permission(PERMISSIONS.admin | PERMISSIONS.income_statistics, json=True)
    def post(self):
        merchant_id =self.current_user.merchant_id
        args = self.get_json_arguments()
        pay_type, ota_id, year, month, value = get_and_valid_arguments(
                args, 'pay_type', 'ota_id', 'year', 'month', 'value'
                )
        remark = args.get('remark', '')
        pay_type, ota_id, year, month, value = int(pay_type), int(ota_id), int(year), int(month), int(value)
        self.valid_args(pay_type, ota_id, year, month, value, remark)

        income = IncomeModel.new(self.db, merchant_id, pay_type, ota_id, year, month, value, remark)

        self.finish_json(result=dict(
            income=income.todict(),
            ))

    def valid_args(self, pay_type, ota_id, year, month, value, remark):
        if pay_type not in [0, 1]:
            raise JsonException(2001, 'invalid pay_type')

        if ota_id not in OTA:
            raise JsonException(2002, 'invalid ota_id')

        if year <= 2000:
            raise JsonException(2003, 'invalid year')

        if month not in range(1, 13):
            raise JsonException(2004, 'invalid month')
