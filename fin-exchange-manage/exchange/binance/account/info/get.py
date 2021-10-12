from typing import Any

from binance_f.model import AccountInformation
from dto.account_dto import AccountDto
from exchange.binance import gen_request_client
from rest.api_function import APIFunction, T


class APIFunctionAccountInfo(APIFunction[AccountDto]):

    def func(self, payload: dict) -> AccountDto:
        result: AccountInformation = gen_request_client().get_account_information()
        return AccountDto(**result.__dict__)


def get_instance():
    return APIFunctionAccountInfo()
