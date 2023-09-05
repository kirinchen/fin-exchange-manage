import traceback

import exchange
from dto.order_create_dto import OrderCreateDto
from infra.enums import PayloadReqKey
from service.order_client_service import OrderClientService
from utils import comm_utils


def run(payload: dict) -> dict:
    try:
        order_client: OrderClientService = exchange.gen_impl_obj(
            exchange_name=PayloadReqKey.exchange.get_val(payload),
            clazz=OrderClientService, **payload)
        dto = OrderCreateDto(**payload)
        return comm_utils.to_dict(order_client.new_order(dto))
    except Exception as e:  # work on python 3.x
        traceback.print_exc()
        return {
            '__error_type': str(type(e)),
            'msg': str(e),
            'traceback': traceback.format_exc()
        }
