from typing import List

from binance_f import RequestClient
from binance_f.model import Order
from sqlalchemy.orm import Session

from dto.order_dto import OrderDto
from exchange.binance import gen_request_client, binance_utils
from service.order_client_service import OrderClientService


class FTXOrderClientService(OrderClientService):

    def __init__(self, **kwargs):
        super(FTXOrderClientService, self).__init__(**kwargs)
        self.client: RequestClient = gen_request_client()

    def list_all_order(self, prd_name: str, orderId: int = None, startTime: int = None, endTime: int = None,
                       limit: int = None) -> List[OrderDto]:
        oods: List[Order] = self.client.get_all_orders(symbol=binance_utils.fix_usdt_symbol(prd_name), limit=limit,
                                                       startTime=startTime, endTime=endTime, orderId=orderId)
        return [binance_utils.convert_order_dto(o) for o in oods]

    def cancel_list_orders(self, symbol: str, currentOds: List[OrderDto]) -> List[OrderDto]:
        pass  # TODO

    def post_limit(self, prd_name: str,onMarketPrice: bool, price: float, quantity: float, positionSide: str, tags: List[str]) -> OrderDto:
        pass  # TODO

    def post_stop_market(self, prd_name: str, price: float, quantity: float, positionSide: str,
                         tags: List[str]) -> OrderDto:
        pass  # TODO

    def post_take_profit(self, prd_name: str, price: float, quantity: float, positionSide: str,
                         tags: List[str]) -> OrderDto:
        pass  # TODO


def get_impl_clazz() -> FTXOrderClientService:
    return FTXOrderClientService
