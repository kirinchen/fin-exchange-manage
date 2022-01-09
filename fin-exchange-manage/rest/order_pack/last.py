from typing import List

import exchange
from dto import order_dto
from dto.order_dto import OrderPackQueryDto
from infra import database
from model import OrderPack
from rest.proxy_controller import PayloadReqKey
from service.order_pack_dao import OrderPackDao
from utils import comm_utils


def run(payload: dict) -> dict:
    with database.session_scope() as session:
        ex = PayloadReqKey.exchange.get_val(payload)
        order_pack_dao: OrderPackDao = exchange.gen_impl_obj(exchange_name=ex, session=session,
                                                             clazz=OrderPackDao)
        PayloadReqKey.clean_default_keys(payload)
        (order_pack, orders) = order_pack_dao.last(payload)
        return {
            "orderPack": order_pack.to_dict(),
            "orders": comm_utils.to_dict([order_dto.convert_entity_to_dto(o) for o in orders])
        }
