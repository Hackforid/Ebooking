# -*- coding: utf-8 -*-


from exception.json_exception import JsonException

from views.base import BtwBaseHandler
from models.order import OrderModel



class PMSNewOrderAPIHandler(BtwBaseHandler):

    def get(self, merchant_id):
        orders, total = OrderModel.get_waiting_orders(self.db, merchant_id)
        self.finish_json(result=dict(
            has_new_order=True if orders else False,
            ))
