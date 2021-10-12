from typing import Any

from dto.account_dto import AccountDto
from rest import api_function


def run(payload: dict) -> AccountDto:
    return api_function.proxy_exchange(payload).func(payload)
