from typing import List

import exchange
from dto.order_dto import OrderDto, OrderPackQueryDto
from infra import database
from model import OrderPack
from rest.proxy_controller import PayloadReqKey
from service.order_client_service import OrderClientService
from service.order_pack_dao import OrderPackDao
from utils import comm_utils
from utils.order_utils import OrderFilter, OrdersInfo


def run(payload: dict) -> dict:
    with database.session_scope() as session:
        ex = PayloadReqKey.exchange.get_val(payload)
        order_pack_dao: OrderPackDao = exchange.gen_impl_obj(exchange_name=ex, session=session,
                                                             clazz=OrderPackDao)
        dto: OrderPackQueryDto = OrderPackQueryDto(**payload)
        ans: List[OrderPack] = order_pack_dao.query(dto)
        return [op.to_dict() for op in ans]
