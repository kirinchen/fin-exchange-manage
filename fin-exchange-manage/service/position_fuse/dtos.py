import abc
from enum import Enum
from typing import List

from dto.order_dto import OrderDto


class StopDto(metaclass=abc.ABCMeta):

    def __init__(self, symbol: str, positionSide: str, tags: List[str]):
        self.symbol: str = symbol
        self.positionSide: str = positionSide
        self.tags: List[str] = tags


class StopState(Enum):
    NO_POS = 'NO_POS'
    LOSS = 'LOSS'
    GUARANTEED = 'GATE'
    PROFIT = 'PROF'


class StopResult:

    def __init__(self, stopState: StopState, orders: List[OrderDto] = list(), active: bool = False,
                 noActiveMsg: str = None,
                 up_to_date: bool = False):
        self.active = active
        self.stopState: str = stopState.value
        self.orders: List[OrderDto] = orders
        self.noActiveMsg: str = noActiveMsg
        self.up_to_date: bool = up_to_date
