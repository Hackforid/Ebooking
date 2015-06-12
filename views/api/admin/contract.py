# -*- coding: utf-8 -*-

from tornado.escape import json_encode, json_decode, url_escape
from tornado import gen

from exception.json_exception import JsonException

from tools.auth import auth_backstage_login, need_backstage_admin
from tools.request_tools import get_and_valid_arguments
from views.base import BackStageHandler

from models.merchant import MerchantModel
from models.cooperate_hotel import CooperateHotelModel
from models.cooperate_roomtype import CooperateRoomTypeModel
from models.contract_hotel import ContractHotelModel
from models.contract_merchant import ContractMerchantModel
from models.contract_roomtype import ContractRoomTypeModel
from models.contract_spec_price import ContractSpecPriceModel

from config import API, BACKSTAGE_ENABLE

from utils import hotel as hotel_util


class MerchantContractAPIHandler(BackStageHandler):

    @auth_backstage_login(json=True)
    @need_backstage_admin(json=True)
    def get(self, merchant_id):

        contract = ContractMerchantModel.get_by_merchant_id(self.db, merchant_id)
        merchant = MerchantModel.get_by_id(self.db, merchant_id)
        self.finish_json(result={
            "contract_merchant": contract.todict() if contract else None,
            "merchant": merchant.todict() if merchant else None,
            })

    @auth_backstage_login(json=True)
    @need_backstage_admin(json=True)
    def post(self, merchant_id):
        contract = ContractMerchantModel.get_by_merchant_id(self.db, merchant_id)
        if contract:
            raise JsonException(1001, 'contract exist')

        contract_args = self.get_json_arguments()

        creator = self.backstage_user_name if BACKSTAGE_ENABLE else 'TEST'
        contract = ContractMerchantModel.new(self.db, creator=creator, **contract_args)

        self.finish_json(result = dict(
            contract_hotel = contract.todict(),
            ))

    @auth_backstage_login(json=True)
    @need_backstage_admin(json=True)
    def put(self, merchant_id):
        contract_args = self.get_json_arguments()

        contract = ContractMerchantModel.get_by_merchant_id(self.db, merchant_id)
        if not contract:
            raise JsonException(1000, 'contract not exist')

        ContractMerchantModel.update(self.db, **contract_args)

        self.finish_json(result = dict(
            contract_hotel = contract.todict(),
            ))


class HotelContractAPIHandler(BackStageHandler):

    @gen.coroutine
    @auth_backstage_login(json=True)
    @need_backstage_admin(json=True)
    def get(self, merchant_id, hotel_id):

        hotel = CooperateHotelModel.get_by_id(self.db, hotel_id)
        if not hotel:
            raise JsonException(4001, 'hotel not found')


        contract_hotel = ContractHotelModel.get_by_hotel(self.db, hotel_id)
        if not contract_hotel:
            contract_hotel = ContractHotelModel.new(self.db, merchant_id=merchant_id, hotel_id=hotel_id, base_hotel_id=hotel.base_hotel_id, weekend="5,6")

        roomtypes = CooperateRoomTypeModel.get_by_hotel_id(self.db, hotel_id)
        contract_roomtypes = ContractRoomTypeModel.get_by_hotel(self.db, hotel_id)


        hotel_dict = hotel.todict()
        roomtype_dicts = [room.todict() for room in roomtypes]
        yield self.merge_base_info(hotel_dict, roomtype_dicts)

        self.finish_json(result=dict(
            hotel=hotel_dict,
            roomtypes=roomtype_dicts,
            contract_hotel=contract_hotel.todict() if contract_hotel else {},
            contract_roomtypes = [c.todict() for c in contract_roomtypes],
            ))


    @gen.coroutine
    def merge_base_info(self, hotel_dict, roomtype_dicts):
        base_hotel, base_roomtypes = yield hotel_util.get_base_hotel_and_roomtypes_info(hotel_dict['base_hotel_id'])

        hotel_dict['base_hotel'] = base_hotel

        for roomtype_dict in roomtype_dicts:
            for base_roomtype in base_roomtypes:
                if base_roomtype['id'] == roomtype_dict['base_roomtype_id']:
                    roomtype_dict['base_roomtype'] = base_roomtype
                    break

    @auth_backstage_login(json=True)
    @need_backstage_admin(json=True)
    def post(self, merchant_id, hotel_id):
        contract_hotel_args = self.get_json_arguments()

        contract_hotel = ContractHotelModel.get_by_hotel(self.db, hotel_id)
        if contract_hotel:
            raise JsonException(1000, 'contract exist')

        contract_hotel = ContractHotelModel.new(self.db, **contract_hotel_args)

        self.finish_json(result = dict(
            contract_hotel = contract_hotel.todict(),
            ))

    @auth_backstage_login(json=True)
    @need_backstage_admin(json=True)
    def put(self, merchant_id, hotel_id):
        contract_hotel_args = self.get_json_arguments()

        contract_hotel = ContractHotelModel.get_by_hotel(self.db, hotel_id)
        if not contract_hotel:
            raise JsonException(1000, 'contract not exist')

        ContractHotelModel.update(self.db, **contract_hotel_args)

        self.finish_json(result = dict(
            contract_hotel = contract_hotel.todict(),
            ))


class RoomTypeContractAPIHandler(BackStageHandler):

    @auth_backstage_login(json=True)
    @need_backstage_admin(json=True)
    def post(self, merchant_id, hotel_id, roomtype_id, pay_type):
        contract_roomtype_args = self.get_json_arguments()

        contract = ContractRoomTypeModel.get_by_hotel_roomtype_pay_type(self.db, hotel_id, roomtype_id, pay_type)
        if contract:
            raise JsonException(1000, 'contract exist')

        contract = ContractRoomTypeModel.new(self.db, hotel_id, roomtype_id, pay_type, **contract_roomtype_args)

        self.finish_json(result=dict(
            contract_roomtype = contract.todict(),
            ))

    @auth_backstage_login(json=True)
    @need_backstage_admin(json=True)
    def put(self, merchant_id, hotel_id, roomtype_id, pay_type):
        contract_roomtype_args = self.get_json_arguments()

        contract = ContractRoomTypeModel.get_by_hotel_roomtype_pay_type(self.db, hotel_id, roomtype_id, pay_type)
        if not contract:
            raise JsonException(1000, 'contract not exist')

        ContractRoomTypeModel.update(self.db, hotel_id, roomtype_id, pay_type, **contract_roomtype_args)

        self.finish_json(result=dict(
            contract_roomtype = contract.todict(),
            ))


class SpecPriceContractAPIHandler(BackStageHandler):

    @auth_backstage_login(json=True)
    @need_backstage_admin(json=True)
    def post(self, merchant_id, hotel_id, roomtype_id, pay_type):
        params = self.get_json_arguments()

        contract = ContractSpecPriceModel.new(self.db, hotel_id, roomtype_id, pay_type, **params)

        self.finish_json(result = dict(
            contract_spec_price = contract.todict(),
            ))

    @auth_backstage_login(json=True)
    @need_backstage_admin(json=True)
    def get(self, merchant_id, hotel_id, roomtype_id, pay_type):
        contracts = ContractSpecPriceModel.get_by_hotel_roomtype_pay_type(self.db, hotel_id, roomtype_id, pay_type)
        self.finish_json(result=dict(
            contract_spec_prices = [c.todict() for c in contracts],
            ))

class SpecPriceContractModifyAPIHandler(BackStageHandler):

    @auth_backstage_login(json=True)
    @need_backstage_admin(json=True)
    def put(self, merchant_id, hotel_id, roomtype_id, contract_id):
        params = self.get_json_arguments()
        contract = ContractSpecPriceModel.get_by_id(self.db, contract_id)
        if not contract:
            raise JsonException(1000, 'contract not found')

        params.update({'hotel_id': hotel_id, 'roomtype_id': roomtype_id})
        ContractSpecPriceModel.update(self.db, contract_id, **params)

        self.finish_json(result = dict(
            contract_spec_price = contract.todict(),
            ))

