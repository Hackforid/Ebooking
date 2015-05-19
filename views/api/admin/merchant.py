# -*- coding: utf-8 -*-

from tornado.escape import json_encode, json_decode, url_escape
from tornado import gen

from exception.json_exception import JsonException

from tools.auth import auth_backstage_login, need_backstage_admin
from tools.url import add_get_params
from tools.request_tools import get_and_valid_arguments
from views.base import BackStageHandler
from models.merchant import MerchantModel
from models.user import UserModel
from models.cooperate_hotel import CooperateHotelModel

from config import API

from tasks.stock import PushHotelTask
from tornado.httpclient import AsyncHTTPClient

class AdminMerchantAPIHandler(BackStageHandler):

    @auth_backstage_login(json=True)
    @need_backstage_admin(json=True)
    def get(self):
        merchants = MerchantModel.get_all(self.db)
        merchants = [merchant.todict() for merchant in merchants]
        self.finish_json(result=dict(
            merchants=merchants
            ))

class AdminMerchantModifyAPIHandler(BackStageHandler):

    @auth_backstage_login(json=True)
    @need_backstage_admin(json=True)
    def post(self):
        args = self.get_json_arguments()
        merchant, root_pwd, admin_pwd = get_and_valid_arguments(args, 'merchant', 'root_pwd', 'admin_pwd')
        name, type = get_and_valid_arguments(merchant, 'name', 'type')

        merchant, admin, root = self.new_merchant(name, type, admin_pwd, root_pwd)

        self.finish_json(result=dict(
            merchant=merchant.todict(),
            admin=admin.todict(),
            root=root.todict(),
            ))

    def new_merchant(self, name, type, admin_pwd, root_pwd):
        merchant = MerchantModel.new_merchant(self.db, name, type)
        admin, root = UserModel.new_admin_root_user(self.db, merchant.id, admin_pwd, root_pwd)
        return merchant, admin, root


    @auth_backstage_login(json=True)
    @need_backstage_admin(json=True)
    def put(self):
        args = self.get_json_arguments()
        merchant, = get_and_valid_arguments(args, 'merchant')
        id, name, type = get_and_valid_arguments(merchant, 'id', 'name', 'type')

        admin_pwd = args.get('admin_pwd', None)
        root_pwd = args.get('root_pwd', None)

        merchant = self.modify_merchant(id, name, type, admin_pwd, root_pwd)

        self.finish_json(result=dict(
            merchant=merchant.todict(),
            ))

    def modify_merchant(self, id, name, type, admin_pwd, root_pwd):
        merchant = MerchantModel.get_by_id(self.db, id)
        if not merchant:
            raise JsonException(errcode=404, errmsg="merchant not fount")
        else:
            merchant.update(self.db, name, type)

        if admin_pwd:
            UserModel.update_password(self.db, merchant.id, 'admin', admin_pwd)
        if root_pwd:
            UserModel.update_password(self.db, merchant.id, 'root', root_pwd)

        return merchant

class AdminMerchantSuspendAPIHandler(BackStageHandler):


    @auth_backstage_login(json=True)
    @need_backstage_admin(json=True)
    def put(self, merchant_id, is_suspend):

        merchant = self.suspend_merchant(merchant_id, is_suspend)
        self.finish_json(result=dict(
            merchant=merchant.todict(),
            ))

    def suspend_merchant(self, merchant_id, is_suspend):
        is_suspend = int(is_suspend)
        merchant = MerchantModel.get_by_id(self.db, merchant_id)
        if not merchant:
            raise JsonException(errcode=404, errmsg="merchant not fount")

        merchant.is_suspend = is_suspend
        CooperateHotelModel.set_suspend_by_merchant_id(self.db, merchant_id, is_suspend)

        self.db.commit()

        PushHotelTask().push_hotel_suspend_by_merchant_id.delay(merchant_id)
        return merchant

class MerchantHotelsAPIHandler(BackStageHandler):

    @gen.coroutine
    @auth_backstage_login(json=True)
    @need_backstage_admin(json=True)
    def get(self, merchant_id):
        start = self.get_query_argument('start', 0)
        limit = self.get_query_argument('limit', 1000)
        name = self.get_query_argument('name', None)
        city_id = self.get_query_argument('city_id', None)
        district_id = self.get_query_argument('district_id', None)
        star = self.get_query_argument('star', None)
        is_online = self.get_query_argument('is_online', None)

        hotels, total = yield self.get_cooped_hotels(merchant_id, start, limit, name, city_id, district_id, star, is_online)
        if hotels is not None and total is not None:
            self.finish_json(result=dict(
                hotels=hotels,
                total=total,
                start=start,
                limit=limit,
                ))
        else:
            raise JsonException(500, 'query error')

    @gen.coroutine
    def get_cooped_hotels(self, merchant_id, start, limit, name, city_id, district_id, star, is_online):
        cooped_base_hotels = self.get_cooped_base_hotels(merchant_id, is_online)
        cooped_base_hotel_ids = [hotel.base_hotel_id for hotel in cooped_base_hotels]
        if not cooped_base_hotel_ids:
            raise gen.Return(([], 0))

        hotels, total = yield self.fetch_hotels(name, city_id, district_id, star, cooped_base_hotel_ids, start, limit)
        if hotels is not None and total is not None:
            yield self.merge_district(hotels)
            self.merge_base_hotel_with_coops(hotels, cooped_base_hotels)
            raise gen.Return((hotels, total))
        else:
            raise gen.Return((None, None))

    def get_cooped_base_hotels(self, merchant_id, is_online):
        return CooperateHotelModel.get_by_merchant_id(self.db, merchant_id, is_online)

    def merge_base_hotel_with_coops(self, base_hotels, cooped_hotels):
        for base in base_hotels:
            for cooped in cooped_hotels:
                if base['id'] == cooped.base_hotel_id:
                    base['base_hotel_id'] = base['id']
                    base['id'] = cooped.id
                    base['is_online'] = cooped.is_online
                    break

    @gen.coroutine
    def fetch_hotels(self, name, city_id, district_id, star, within_ids, start, limit):
        params = {'name': url_escape(name) if name else None, 'city_id': city_id, 'district_id': district_id, 'star': star, 'start': start, 'limit': limit}

        if within_ids:
            params['within_ids'] = url_escape(json_encode(within_ids))
        url = add_get_params(API['POI'] + u'/api/hotel/search/', params)
        print 'url=', url

        resp = yield AsyncHTTPClient().fetch(url)

        r = json_decode(resp.body)

        if r and r['errcode'] == 0:
            hotels = r['result']['hotels']
            total = r['result']['total']
            raise gen.Return((hotels, total))
        else:
            raise gen.Return((None, None))

    @gen.coroutine
    def merge_district(self, hotels):
        district_ids = [hotel['district_id'] for hotel in hotels]
        district_ids = {}.fromkeys(district_ids).keys()

        districts = yield self.fetch_districts(district_ids)

        for hotel in hotels:
            for district in districts:
                if hotel['district_id'] == district['id']:
                    hotel['district_name'] = district['name']
                    break
        raise gen.Return()

    @gen.coroutine
    def fetch_districts(self, district_ids):
        url = API['POI'] + '/api/district/?district_ids=' + url_escape(json_encode(district_ids))
        print url

        resp = yield AsyncHTTPClient().fetch(url)
        r = json_decode(resp.body)
        if r and r['errcode'] == 0:
            districts = r['result']['districts']
            raise gen.Return(districts)
        else:
            raise gen.Return([])

