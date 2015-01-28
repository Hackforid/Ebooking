# -*- coding: utf-8 -*-

from tornado import gen
from tornado.httpclient import AsyncHTTPClient
from tornado.escape import json_encode, json_decode

from config import API
from views.base import BtwBaseHandler
from models.merchant import MerchantModel 

class MerchantListAPIHandler(BtwBaseHandler):

    def get(self):
        merchants = MerchantModel.get_all(self.db)
        self.finish_json(result=dict(
            merchants=[merchant.todict() for merchant in merchants]
            ))
