import abc
from abc import ABC
from typing import List

from dto.position_dto import PositionDto, PositionFilter
from service.base_exchange_abc import BaseExchangeAbc
from utils import position_utils


class PositionClientService(BaseExchangeAbc, ABC):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)



    def get_abc_clazz(self) -> object:
        return PositionClientService

    @abc.abstractmethod
    def list_all(self, prd_name: str = None) -> List[PositionDto]:
        raise NotImplementedError('list_all')

    def query(self, position_filter: PositionFilter) -> List[PositionDto]:
        return position_utils.filter_position(self.list_all(position_filter.symbol), position_filter)

    def find_one(self, symbol: str, positionSide: str) -> PositionDto:
        return position_utils.find_position_one(self.list_all(symbol), symbol, positionSide)

    def get_max_order_amt(self, symbol: str, positionSide: str, price: float) -> float:
        pos = self.find_one(symbol, positionSide)
        return pos.maxNotionalValue / price

    @abc.abstractmethod
    def close(self, prd_name: str, positionSide: str, amount: float) -> any:
        raise NotImplementedError('close')
