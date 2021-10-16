from typing import List

import exchange
from dto.order_dto import OrderDto
from rest.proxy_controller import PayloadReqKey
from service.order_client_service import OrderClientService
from utils.order_utils import OrderFilter


def run(payload: dict) -> List[OrderDto]:
    ex = PayloadReqKey.exchange.get_val(payload)
    order_service: OrderClientService = exchange.get_service(exchange_name=ex, clazz=OrderClientService)
    order_filter: OrderFilter = OrderFilter(**payload)
    return order_service.query_order(order_filter)
