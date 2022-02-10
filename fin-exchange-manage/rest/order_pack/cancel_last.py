from typing import List

import exchange
from dto import order_dto
from dto.order_dto import OrderDto
from infra import database
from model import OrderPack
from rest.proxy_controller import PayloadReqKey
from service.order_client_service import OrderClientService
from service.order_pack_dao import OrderPackDao
from utils import comm_utils


def run(payload: dict) -> dict:
    with database.session_scope() as session:
        ex = PayloadReqKey.exchange.get_val(payload)
        orderClient: OrderClientService = exchange.gen_impl_obj(exchange_name=ex, session=session,
                                                                clazz=OrderClientService, **payload)
        order_pack_dao: OrderPackDao = exchange.gen_impl_obj(exchange_name=ex, session=session,
                                                             clazz=OrderPackDao, **payload)
        PayloadReqKey.clean_default_keys(payload)
        filter_map: dict = payload.get('filter_map')
        ans = dict()
        for k, v in filter_map.items():
            ans[k] = cancel_one(orderClient, v, order_pack_dao)
        return ans


def cancel_one(orderClient: OrderClientService, f_dict: dict, order_pack_dao: OrderPackDao) -> object:
    (order_pack, orders) = order_pack_dao.last(f_dict)
    order_pack: OrderPack = order_pack
    orders: List[OrderDto] = [order_dto.convert_entity_to_dto(o) for o in orders]
    if not order_pack:
        return None
    return orderClient.clean_orders(symbol=order_pack.prd_name, currentOds=orders)
