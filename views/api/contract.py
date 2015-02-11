# -*- coding: utf-8 -*-


from tools.auth import auth_login, auth_permission
from tools.request_tools import get_and_valid_arguments
from views.base import BtwBaseHandler
from exception.json_exception import JsonException

from constants import PERMISSIONS

from models.contract import ContractModel



class ContractAPIHandler(BtwBaseHandler):

    @auth_login(json=True)
    @auth_permission(PERMISSIONS.admin | PERMISSIONS.income_statistics, json=True)
    def get(self):
        contracts = ContractModel.get_by_merchant(self.db, self.merchant.id)

        self.finish_json(result=dict(
            contracts=[contract.todict() for contract in contracts],
            ))

    @auth_login(json=True)
    @auth_permission(PERMISSIONS.root, json=True)
    def post(self):
        args = self.get_json_arguments()
        commission = None
        name, type, bank_name, bank_account_id, bank_account_name = get_and_valid_arguments(args,
                'name', 'type', 'bank_name', 'bank_account_id', 'bank_account_name')
        type = int(type)
        if type ==  ContractModel.PAY_TYPE_ARRIVE:
            commission, = get_and_valid_arguments(args, 'commission')

        self.valid_args(name, type, commission, bank_name, bank_account_id, bank_account_name)

        contract = ContractModel.get_by_merchant_and_type(self.db, self.merchant.id, type)
        if contract:
            raise JsonException(2000, 'contract exist')

        contract = ContractModel.new(self.db, self.merchant.id, name, type, commission, bank_name, bank_account_id, bank_account_name)

        self.finish_json(result=dict(
            contract=contract.todict(),
            ))

    def valid_args(self, name, type, commission, bank_name, bank_account_id, bank_account_name):
        if type not in [ContractModel.PAY_TYPE_ARRIVE, ContractModel.PAY_TYPE_PRE]:
            raise JsonException(1000, 'invalid arg: type')


    @auth_login(json=True)
    @auth_permission(PERMISSIONS.root, json=True)
    def put(self):
        args = self.get_json_arguments()
        commission = None
        id, name, bank_name, bank_account_id, bank_account_name = get_and_valid_arguments(args,
                'id', 'name', 'bank_name', 'bank_account_id', 'bank_account_name')

        contract = ContractModel.get_by_id_and_merchant(self.db, id, self.merchant.id)
        if not contract:
            raise JsonException(2000, 'contract not found')

        contract.name = name
        contract.bank_name = bank_name
        contract.bank_account_id = bank_account_id
        contract.bank_account_name = bank_account_name

        if contract.type ==  ContractModel.PAY_TYPE_ARRIVE:
            commission, = get_and_valid_arguments(args, 'commission')
            contract.commission = commission

        self.db.commit()

        self.finish_json(result=dict(
            contract=contract.todict(),
            ))

