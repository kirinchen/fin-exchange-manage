import abc
from abc import ABC

from infra.enums import CandlestickInterval
from service.base_exchange_abc import BaseExchangeAbc


class MarketClientService(BaseExchangeAbc, ABC):

    def get_abc_clazz(self) -> object:
        return MarketClientService

    @abc.abstractmethod
    def get_candlestick_data(self, prd_name: str, interval: CandlestickInterval,
                             startTime: int = None, endTime: int = None, limit: int = None) -> any:
        raise NotImplementedError('get_candlestick_data')
