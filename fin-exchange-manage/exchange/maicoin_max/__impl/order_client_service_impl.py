from typing import List

from sqlalchemy.orm import Session

from binance_f import RequestClient
from binance_f.model import Order
from dto.order_dto import OrderDto
from exchange.binance import gen_request_client, binance_utils
from service.order_client_service import OrderClientService


class MaxOrderClientService(OrderClientService):

    def __init__(self, exchange_name: str, session: Session = None):
        super(MaxOrderClientService, self).__init__(exchange_name, session)
        self.client: RequestClient = gen_request_client()

    def list_all_order(self, symbol: str, orderId: int = None, startTime: int = None, endTime: int = None,
                       limit: int = None) -> List[OrderDto]:
        oods: List[Order] = self.client.get_all_orders(symbol=binance_utils.fix_usdt_symbol(symbol), limit=limit,
                                                       startTime=startTime, endTime=endTime, orderId=orderId)
        return [binance_utils.convert_order_dto(o) for o in oods]

    def cancel_list_orders(self, symbol: str, orderIdList: List[str]):
        pass  # TODO

    def post_limit(self, symbol: str, price: float, quantity: float, positionSide: str, tags: List[str]) -> OrderDto:
        pass  # TODO

    def post_stop_market(self, symbol: str, price: float, quantity: float, positionSide: str,
                         tags: List[str]) -> OrderDto:
        pass  # TODO

    def post_take_profit(self, symbol: str, price: float, quantity: float, positionSide: str,
                         tags: List[str]) -> OrderDto:
        pass  # TODO


def get_impl_clazz() -> MaxOrderClientService:
    return MaxOrderClientService
