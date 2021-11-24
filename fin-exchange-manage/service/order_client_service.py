import abc
from abc import ABC
from typing import List

from sqlalchemy.orm import Session

from dto.order_dto import OrderDto
from service.base_exchange_abc import BaseExchangeAbc
from utils import order_utils
from utils.order_utils import OrderFilter, OrdersInfo


class OrderClientService(BaseExchangeAbc, ABC):

    def get_abc_clazz(self) -> object:
        return OrderClientService

    def query_order(self, filter_obj: OrderFilter) -> OrdersInfo:
        orders = self.list_all_order(symbol=filter_obj.symbol, limit=filter_obj.limit,
                                     startTime=filter_obj.updateStartTime, endTime=filter_obj.updateEndTime)
        return order_utils.filter_order(oods=orders, ft=filter_obj)

    def clean_orders(self, symbol: str, currentOds: List[OrderDto]) -> List[OrderDto]:
        try:
            if currentOds is None:
                return list()
            if len(currentOds) <= 0:
                return list()
            self.cancel_list_orders(symbol=symbol,
                                    orderIdList=[od.clientOrderId for od in currentOds])
            return currentOds
        except Exception as e:  # work on python 3.x
            print('Failed to upload to ftp: ' + str(e))

    @abc.abstractmethod
    def cancel_list_orders(self, symbol: str, orderIdList: List[str]):
        raise NotImplementedError('cancel_list_orders')

    @abc.abstractmethod
    def list_all_order(self, symbol: str, orderId: int = None, startTime: int = None,
                       endTime: int = None, limit: int = None) -> List[OrderDto]:
        raise NotImplementedError('not impl')
