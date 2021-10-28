from typing import Any

from dto.account_dto import AccountDto
from exchange.maicoin_max import gen_request_client
from rest.api_function import APIFunction, T


class APIFunctionAccountInfo(APIFunction[AccountDto]):

    def func(self, payload: dict) -> AccountDto:
        result: object = gen_request_client().get_private_account_balances()
        return result


def get_instance():
    return APIFunctionAccountInfo()
