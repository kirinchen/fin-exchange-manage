import abc
from abc import ABC
from datetime import datetime
from typing import List, Dict, Any

from binance_f.model import Candlestick

from dto.market_dto import CandlestickDto
from infra.enums import CandlestickInterval
from service.base_exchange_abc import BaseExchangeAbc


class MarketClientService(BaseExchangeAbc, ABC):

    def get_abc_clazz(self) -> object:
        return MarketClientService

    @abc.abstractmethod
    def get_candlestick_data(self, prd_name: str, interval: CandlestickInterval,
                             startTime: datetime = None,
                             endTime: datetime = None, limit: int = None) -> List[CandlestickDto]:
        raise NotImplementedError('get_candlestick_data')

    def get_multiple_candlestick_data(self, prd_name_list: List[str], interval: CandlestickInterval,
                                      startTime: datetime = None,
                                      endTime: datetime = None, limit: int = None) -> Dict[str, List[CandlestickDto]]:
        ans: Dict[str, List[CandlestickDto]] = dict()
        for prd_name in prd_name_list:
            ans[prd_name] = self.get_candlestick_data(prd_name, interval, startTime, endTime, limit)
        return ans

    @abc.abstractmethod
    def get_exchange_info(self) -> Any:
        raise NotImplementedError('get_exchange_info')
