import traceback

import exchange
from dto.order_create_dto import OrderCreateBatchDto
from infra.enums import PayloadReqKey
from service.order_client_service import OrderClientService
from utils import comm_utils


def run(payload: dict) -> dict:
    order_client: OrderClientService = exchange.gen_impl_obj(
        exchange_name=PayloadReqKey.exchange.get_val(payload),
        clazz=OrderClientService, **payload)
    ans = dict()
    dto = OrderCreateBatchDto(**payload)
    for key, value in dto.body.items():
        try:
            ans[key] = comm_utils.to_dict(order_client.new_order(value))
        except Exception as e:  # work on python 3.x
            traceback.print_exc()
            ans[key] = {
                '__error_type': str(type(e)),
                'msg': str(e),
                'traceback': traceback.format_exc()
            }
    return ans
