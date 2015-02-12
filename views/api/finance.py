# -*- coding: utf-8 -*-

import json
from datetime import date

from views.base import BtwBaseHandler
from models.order import OrderModel
from models.income import IncomeModel
from models.contract import ContractModel
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
        ota_ids = self.get_query_argument('ota_ids', None)
        pay_type = int(self.get_query_argument('pay_type', 1))
        merchant_id =self.current_user.merchant_id

        if ota_ids:
            ota_ids = json.loads(ota_ids)

        orders = self.get_order_in_date(merchant_id, year, month, pay_type, ota_ids)
        incomes = self.get_income_record_in_date(merchant_id, year, month, pay_type, ota_ids)

        if pay_type == ContractModel.PAY_TYPE_ARRIVE:
            self.deal_agency(orders)

        self.finish_json(result=dict(
            orders=[order.todict() for order in orders],
            incomes=[income.todict() for income in incomes],
            ))

    def deal_agency(self, orders):
        commission = self.get_commission(self.merchant.id)
        for order in orders:
            order.total_price = order.total_price * commission

    def get_order_in_date(self, merchant_id, year, month, pay_type, ota_ids=None):
        orders = OrderModel.get_success_order_by_checkout_date_in_month(self.db,
                merchant_id, year, month, pay_type, ota_ids)
        return orders

    def get_income_record_in_date(self, merchant_id, year, month, pay_type, ota_ids=None):
        incomes = IncomeModel.get_in_month(self.db, merchant_id, year, month, pay_type, ota_ids)
        return incomes

    def get_commission(self, merchant_id):
        contract = ContractModel.get_by_merchant_and_type(self.db, merchant_id, ContractModel.PAY_TYPE_ARRIVE)
        return contract.commission / 100.0 if contract else 0




class IncomeAPIHandler(BtwBaseHandler):

    @auth_login(json=True)
    @auth_permission(PERMISSIONS.admin | PERMISSIONS.income_statistics, json=True)
    def post(self):
        merchant_id =self.current_user.merchant_id
        args = self.get_json_arguments()
        pay_type, ota_ids, year, month, value = get_and_valid_arguments(
                args, 'pay_type', 'ota_ids', 'year', 'month', 'value'
                )
        remark = args.get('remark', '')
        self.valid_args(pay_type, ota_ids, year, month, value, remark)

        income = IncomeModel.new(self.db, merchant_id, pay_type, min(ota_ids), year, month, value, remark)

        self.finish_json(result=dict(
            income=income.todict(),
            ))

    def valid_args(self, pay_type, ota_ids, year, month, value, remark):
        if pay_type not in [0, 1]:
            raise JsonException(2001, 'invalid pay_type')

        #if ota_id not in OTA:
            #raise JsonException(2002, 'invalid ota_id')

        if year <= 2000:
            raise JsonException(2003, 'invalid year')

        if month not in range(1, 13):
            raise JsonException(2004, 'invalid month')
