import abc
from abc import ABC
from typing import List

from dto.position_dto import PositionDto, PositionFilter
from service.base_exchange_abc import BaseExchangeAbc
from utils import position_utils


class PositionClientService(BaseExchangeAbc, ABC):

    def get_abc_clazz(self) -> object:
        return PositionClientService

    @abc.abstractmethod
    def list_all(self) -> List[PositionDto]:
        raise NotImplementedError('list_all')

    def query(self, position_filter: PositionFilter) -> List[PositionDto]:
        return position_utils.filter_position(self.list_all(), position_filter)

    def find_one(self, symbol: str, positionSide: str) -> PositionDto:
        return position_utils.find_position_one(self.list_all(), symbol, positionSide)
