from typing import List

from dto.order_dto import OrderDto
from infra.enums import OrderType
from service.order_client_service import OrderClientService
from utils import reflection_util


class OrderCreateDto:

    def __init__(self, **kwargs):
        self.prd_name: str = None
        self.ordertype: str = None
        self.positionSide: str = None
        self.quantity: float = -1.0
        self.marketPrice: float = -1.0
        self.price: float = -1.0
        self.tags: List[str] = list()
        reflection_util.merge(kwargs, self)

    def call(self, service: OrderClientService) -> OrderDto:
        if self.ordertype == OrderType.LIMIT:
            return service.post_limit(prd_name=self.prd_name,
                                      onMarketPrice=self.marketPrice,
                                      price=self.price,
                                      quantity=self.quantity,
                                      positionSide=self.positionSide,
                                      tags=self.tags
                                      )
        if self.ordertype == OrderType.STOP_MARKET:
            return service.post_stop_market(prd_name=self.prd_name,
                                            quantity=self.quantity,
                                            positionSide=self.positionSide,
                                            tags=self.tags,
                                            price=self.price
                                            )
        if self.ordertype == OrderType.TAKE_PROFIT:
            return service.post_take_profit(prd_name=self.prd_name,
                                            quantity=self.quantity,
                                            price=self.price,
                                            positionSide=self.positionSide,
                                            tags=self.tags
                                            )
        raise NotImplementedError(self.ordertype + ' : not impl ')
