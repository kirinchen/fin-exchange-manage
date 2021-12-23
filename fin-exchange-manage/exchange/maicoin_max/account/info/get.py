from typing import Any, List

from dto.account_dto import AccountDto
from exchange.maicoin_max import gen_request_client, max_utils
from maicoin_max.dto.position import Position
from rest.api_function import APIFunction, T


class APIFunctionAccountInfo(APIFunction[AccountDto]):

    def func(self, payload: dict) -> AccountDto:
        client = gen_request_client()
        result: List[Position] = client.get_private_account_balances()
        # result: object = gen_request_client().get_public_all_tickers()
        return max_utils.convert_account_dto(client, result)


def get_instance():
    return APIFunctionAccountInfo()
