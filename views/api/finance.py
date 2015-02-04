# -*- coding: utf-8 -*-

from datetime import date

from tornado import gen
from tornado.httpclient import AsyncHTTPClient
from tornado.escape import json_encode, json_decode

from config import API
from views.base import BtwBaseHandler
from models.order import OrderModel
from models.income import IncomeModel

class FinanceAPIHandler(BtwBaseHandler):

    def get(self):
        today = date.today()
        year = self.get_query_argument('year', today.year)
        month = self.get_query_argument('month', today.month)
        ota_id = self.get_query_argument('ota_id', None)
        pay_type =self.get_query_argument('pay_type', 1)
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
