from typing import List

import exchange
from dto.order_dto import OrderDto
from infra import database
from rest.proxy_controller import PayloadReqKey
from service.order_client_service import OrderClientService
from utils.order_utils import OrderFilter, OrdersInfo


def run(payload: dict) -> dict:
    with database.session_scope() as session:
        ex = PayloadReqKey.exchange.get_val(payload)
        order_service: OrderClientService = exchange.gen_impl_obj(exchange_name=ex, session=session,
                                                                  clazz=OrderClientService)
        order_filter: OrderFilter = OrderFilter(**payload)
        info: OrdersInfo = order_service.query_order(order_filter)
        return info.to_struct()
