import asyncio
from typing import Any, List

from dto.account_dto import AccountDto
from exchange.bitfinex import gen_request_client

from rest.api_function import APIFunction, T


class APIFunctionAccountInfo(APIFunction[AccountDto]):

    def func(self, payload: dict) -> AccountDto:
        client = gen_request_client()
        loop = asyncio.get_event_loop()
        coroutine = client.rest.get_wallets()
        result = loop.run_until_complete(coroutine)

        # result: object = gen_request_client().get_public_all_tickers()
        return result


def get_instance():
    return APIFunctionAccountInfo()
