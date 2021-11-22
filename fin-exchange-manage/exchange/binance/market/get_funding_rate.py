from typing import Any

from binance_f.model import AccountInformation
from dto.account_dto import AccountDto
from exchange.binance import gen_request_client, binance_utils
from rest.api_function import APIFunction, T


class APIFunctionGetFundingRate(APIFunction[dict]):

    def func(self, payload: dict) -> dict:
        symbol: str = payload.get("symbol")
        result: dict = gen_request_client().get_funding_rate(symbol=binance_utils.fix_usdt_symbol(symbol))
        return result


def get_instance():
    return APIFunctionGetFundingRate()
