import exchange
from infra import database

from rest.proxy_controller import PayloadReqKey
from service.order_client_service import OrderClientService
from utils import comm_utils
from utils.order_utils import OrderFilter


def run(payload: dict) -> dict:
    with database.session_scope() as session:
        order_client: OrderClientService = exchange.gen_impl_obj(exchange_name=PayloadReqKey.exchange.get_val(payload),
                                                                 clazz=OrderClientService, session=session)
        order_filter = OrderFilter(**payload)
        result = order_client.cancel_orders_by(order_filter)
        return comm_utils.to_dict(result)
