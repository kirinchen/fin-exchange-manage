import abc
from abc import ABC
from typing import List

from dto.trade_dto import TradeSet, TradeDto
from service.base_exchange_abc import BaseExchangeAbc
from utils import trade_utils, direction_utils


class TradeClientService(BaseExchangeAbc, ABC):

    def get_abc_clazz(self) -> object:
        return TradeClientService

    @abc.abstractmethod
    def fetch_recent_list(self, symbol: str, limit: int) -> List[TradeDto]:
        raise NotImplementedError('fetch_recent_list')

    def fetch_recent_set(self, symbol: str, limit: int, time_maped: bool = False) -> TradeSet:
        return trade_utils.gen_subtotal_result(self.fetch_recent_list(symbol, limit), time_maped)

    def get_last_price(self, symbol: str) -> float:
        data = self.fetch_recent_set(symbol=symbol, limit=10, time_maped=False)
        return data.all.lastPrice

    def get_last_rise_price(self, positionSide: str, symbol: str, buffRate=1.00002) -> float:
        lastPrice = self.get_last_price(symbol=symbol)
        return direction_utils.rise_price(positionSide, lastPrice, buffRate)

    def get_last_fall_price(self, positionSide: str, symbol: str, buffRate=1.00002) -> float:
        lastPrice = self.get_last_price(symbol=symbol)
        return direction_utils.fall_price(positionSide, lastPrice, buffRate)
