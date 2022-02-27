from datetime import datetime
from typing import List, Any

from maicoin_max.client import Client

from dto.market_dto import CandlestickDto
from exchange.maicoin_max import gen_request_client
from infra.enums import CandlestickInterval
from service.market_client_sevice import MarketClientService


class MaxMarketClientService(MarketClientService):

    def __init__(self, **kwargs):
        super(MaxMarketClientService, self).__init__(**kwargs)
        self.client: Client = gen_request_client()

    def _candlestick_interval_minute(self, interval: CandlestickInterval) -> int:
        return {
            CandlestickInterval.MIN1: 1,
            CandlestickInterval.MIN3: 3,
            CandlestickInterval.MIN5: 5,
            CandlestickInterval.HOUR1: 60,
            CandlestickInterval.HOUR2: 60 * 2,
            CandlestickInterval.HOUR4: 60 * 4,
            CandlestickInterval.HOUR6: 60 * 6,
            CandlestickInterval.HOUR8: 60 * 8,
            CandlestickInterval.HOUR12: 60 * 12,
            CandlestickInterval.DAY1: 60 * 24,
            CandlestickInterval.DAY3: 60 * 24 * 3
        }.get(interval)

    def _clac_limit(self, period:int,range_time:float,org_limit:int)->int:
        TODO: support

    def get_candlestick_data(self, prd_name: str, interval: CandlestickInterval, startTime: datetime = None,
                             endTime: datetime = None, limit: int = None) -> List[CandlestickDto]:
        self.client.get_public_k_line(pair=prd_name, limit=limit, startTime)
        return [binance_utils.convert_candlestick_dto(r) for r in result]

    def get_exchange_info(self) -> Any:
        return self.client.get_exchange_information()


def get_impl_clazz() -> MaxMarketClientService:
    return MaxMarketClientService
