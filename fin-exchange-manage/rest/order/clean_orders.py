from typing import List

import exchange
from dto.order_dto import OrderDto
from infra.enums import PayloadReqKey
from service.order_client_service import OrderClientService
from utils import comm_utils


class CleanOdsDto:

    def __init__(self, symbol: str, currentOds: List[dict], **kwargs):
        self.symbol = symbol
        self.currentOds = currentOds

    def get_current_ods_dto(self) -> List[OrderDto]:
        return [OrderDto(**d) for d in self.currentOds]


def run(payload: dict) -> dict:
    order_client: OrderClientService = exchange.gen_impl_obj(exchange_name=PayloadReqKey.exchange.get_val(payload),
                                                             clazz=OrderClientService, **payload)
    clean_ods_dto = CleanOdsDto(**payload)
    result = order_client.clean_orders(clean_ods_dto.symbol, clean_ods_dto.get_current_ods_dto())
    return comm_utils.to_dict(result)
