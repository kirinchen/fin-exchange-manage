from typing import List

from model import Order
from utils import reflection_util, entity_utils


class OrderDto:

    def __init__(self,
                 clientOrderId=""
                 , cumQuote=0.0
                 , executedQty=None
                 , orderId=None
                 , origQty=None
                 , price=None
                 , side=None
                 , status=None
                 , stopPrice=None
                 , symbol=""
                 , type=None
                 , updateTime=0
                 , avgPrice=0.0
                 , origType=""
                 , positionSide=""
                 , activatePrice=None
                 , priceRate=None
                 , closePosition=None
                 , updateAt=None, **kwargs
                 ):
        self.clientOrderId = clientOrderId
        self.cumQuote = cumQuote
        self.executedQty = executedQty
        self.orderId = orderId
        self.origQty = origQty
        self.price = price
        self.side = side
        self.status = status
        self.stopPrice = stopPrice
        self.symbol = symbol
        self.type = type
        self.updateTime = updateTime
        self.avgPrice = avgPrice
        self.origType = origType
        self.positionSide = positionSide
        self.activatePrice = activatePrice
        self.priceRate = priceRate
        self.closePosition = closePosition
        self.updateAt: str = updateAt


class OrderPackQueryDto:

    def __init__(self, **kwargs):
        self.uid_list: List[str] = None
        self.exchange: str = None
        self.order_strategy: str = None
        self.tags: List[str] = None
        self.attach_name: str = None
        self.side: str = None
        self.prd_name: str = None
        self.positionSide: str = None
        reflection_util.merge(kwargs, self)

    def to_query_eq_dict(self) -> dict:
        ans = dict()
        for k, v in self.__dict__.items():
            if k.startswith('_'):
                continue
            if isinstance(v, str):
                ans[k] = v
        return ans


def convert_entity_to_dto(e: Order) -> OrderDto:
    ans = OrderDto(**e.__dict__)
    ans.symbol = e.prd_name
    return ans
