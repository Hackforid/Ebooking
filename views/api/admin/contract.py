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
from models.contract_roomtype import ContractRoomTypeModel

from config import API, BACKSTAGE_ENABLE

from utils import hotel as hotel_util

class HotelContractAPIHandler(BackStageHandler):


    @gen.coroutine
    @auth_backstage_login(json=True)
    @need_backstage_admin(json=True)
    def get(self, merchant_id, hotel_id):

        hotel = CooperateHotelModel.get_by_id(self.db, hotel_id)
        if not hotel:
            raise JsonException(4001, 'hotel not found')


        contract_hotel = ContractHotelModel.get_by_hotel(self.db, hotel_id)

        roomtypes = CooperateRoomTypeModel.get_by_hotel_id(self.db, hotel_id)
        contract_roomtypes = ContractRoomTypeModel.get_by_hotel(self.db, hotel_id)

        hotel_dict = hotel.todict()
        roomtype_dicts = [room.todict() for room in roomtypes]
        yield self.merge_base_info(hotel_dict, roomtype_dicts)

        self.finish_json(result=dict(
            hotel=hotel_dict,
            roomtypes=roomtype_dicts,
            contract_hotel=contract_hotel.todict() if contract_hotel else {},
            contract_roomtypes = [c.todict() for c in contract_roomtypes]
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

        creator = self.backstage_user_name if BACKSTAGE_ENABLE else 'TEST'
        contract_hotel = ContractHotelModel.new(self.db, creator=creator, **contract_hotel_args)

        self.finish_json(result = dict(
            contract_hotel = contract_hotel.todict(),
            ))




