from typing import Any, List

from dto.order_dto import OrderDto
from rest import api_function


def run(payload: dict) -> List[OrderDto]:
    return api_function.proxy_exchange(payload).func(payload)
