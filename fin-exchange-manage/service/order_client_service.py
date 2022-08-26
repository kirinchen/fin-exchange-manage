import abc
from abc import ABC
from typing import List

from sqlalchemy.orm import Session

import exchange
from dto.order_create_dto import OrderCreateDto
from dto.order_dto import OrderDto
from infra.enums import OrderStatus
from service.base_exchange_abc import BaseExchangeAbc
from service.position_client_service import PositionClientService
from service.product_dao import ProductDao
from utils import order_utils
from utils.order_utils import OrderFilter, OrdersInfo


class OrderClientService(BaseExchangeAbc, ABC):

    def __init__(self, **kwargs):
        super(OrderClientService, self).__init__(**kwargs)
        self.productDao: ProductDao = None
        self.positionClient: PositionClientService = None

    def after_init(self):
        self.productDao: ProductDao = self.get_ex_obj(ProductDao)
        self.positionClient: PositionClientService = self.get_ex_obj(PositionClientService)

    def get_abc_clazz(self) -> object:
        return OrderClientService

    def query_order(self, filter_obj: OrderFilter) -> OrdersInfo:
        orders = self.list_all_order(prd_name=filter_obj.symbol, limit=filter_obj.limit,
                                     startTime=filter_obj.updateStartTime, endTime=filter_obj.updateEndTime)
        return order_utils.filter_order(oods=orders, ft=filter_obj)

    def cancel_orders_by(self, order_filter: OrderFilter) -> List[OrderDto]:
        if not order_filter.symbol:
            raise TypeError('symbol can not null')
        result = self.query_order(order_filter)
        return self.clean_orders(order_filter.symbol, result.orders)

    def clean_orders(self, symbol: str, currentOds: List[OrderDto]) -> List[OrderDto]:
        try:
            if currentOds is None:
                return list()
            currentOds = [x for x in currentOds if x.status == OrderStatus.NEW]
            if len(currentOds) <= 0:
                return list()

            self.cancel_list_orders(symbol=symbol,
                                    currentOds=currentOds)
            return currentOds
        except Exception as e:  # work on python 3.x
            print('Failed to upload to ftp: ' + str(e))

    def new_order(self, dto: OrderCreateDto) -> OrderDto:
        return dto.call(service=self)

    @abc.abstractmethod
    def cancel_list_orders(self, symbol: str, currentOds: List[OrderDto]) -> List[OrderDto]:
        raise NotImplementedError('cancel_list_orders')

    @abc.abstractmethod
    def list_all_order(self, prd_name: str, orderId: int = None, startTime: int = None,
                       endTime: int = None, limit: int = None) -> List[OrderDto]:
        raise NotImplementedError('not impl')

    @abc.abstractmethod
    def post_limit(self, prd_name: str, onMarketPrice: bool, price: float, quantity: float, positionSide: str,
                   tags: List[str]) -> OrderDto:
        raise NotImplementedError('post_limit')

    @abc.abstractmethod
    def post_stop_market(self, prd_name: str, price: float, quantity: float, positionSide: str,
                         tags: List[str]) -> OrderDto:
        raise NotImplementedError('post_stop_market')

    @abc.abstractmethod
    def post_take_profit(self, prd_name: str, price: float, quantity: float, positionSide: str,
                         tags: List[str]) -> OrderDto:
        raise NotImplementedError('post_take_profit')
