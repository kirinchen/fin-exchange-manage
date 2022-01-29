from typing import List, Any

from maicoin_max.client import Client
from sqlalchemy.orm import Session

from dto.order_dto import OrderDto
from exchange.maicoin_max import gen_request_client, max_utils
from service.order_client_service import OrderClientService


class MaxOrderClientService(OrderClientService):

    def __init__(self, exchange_name: str, session: Session = None):
        super(MaxOrderClientService, self).__init__(exchange_name, session)
        self.client: Client = gen_request_client()

    def list_all_order(self, prd_name: str, orderId: int = None, startTime: int = None, endTime: int = None,
                       limit: int = None) -> List[OrderDto]:
        oods: List[Any] = self.client.get_private_order_history(pair=prd_name, state=["done"])
        return [max_utils.convert_order_dto(od) for od in oods]

    def cancel_list_orders(self, symbol: str, currentOds: List[OrderDto]) -> List[OrderDto]:
        pass  # TODO

    def post_limit(self, prd_name: str, onMarketPrice: bool, price: float, quantity: float, positionSide: str,
                   tags: List[str]) -> OrderDto:
        pass  # TODO

    def post_stop_market(self, prd_name: str, price: float, quantity: float, positionSide: str,
                         tags: List[str]) -> OrderDto:
        pass  # TODO

    def post_take_profit(self, prd_name: str, price: float, quantity: float, positionSide: str,
                         tags: List[str]) -> OrderDto:
        pass  # TODO


def get_impl_clazz() -> MaxOrderClientService:
    return MaxOrderClientService
