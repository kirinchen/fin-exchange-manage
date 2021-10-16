from abc import ABC
from typing import List

from dto.order_dto import OrderDto
from utils import order_utils
from utils.order_utils import OrderFilter, OrdersInfo


class OrderClientService(ABC):

    def __init__(self, exchange: str):
        self.exchange = exchange

    def query_order(self, filter_obj: OrderFilter) -> OrdersInfo:
        orders = self.list_all_order(symbol=filter_obj.symbol, limit=filter_obj.limit,
                                     startTime=filter_obj.updateStartTime, endTime=filter_obj.updateEndTime)
        return order_utils.filter_order(oods=orders, ft=filter_obj)

    def list_all_order(self, symbol: str, orderId: int = None, startTime: int = None,
                       endTime: int = None, limit: int = None) -> List[OrderDto]:
        raise NotImplementedError('not impl')
