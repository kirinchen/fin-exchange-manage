import os
from typing import Any

from dto.account_dto import AccountDto
from rest import api_function
from utils import path_utils


def run(payload: dict) -> AccountDto:
    return api_function.proxy_exchange(payload).func(payload)


def invoke(exchange: str) -> AccountDto:
    payload: dict = path_utils.get_rest_req_dict(exchange, __file__)
    return run(payload)
