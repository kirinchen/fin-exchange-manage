from datetime import datetime, timezone
from typing import List, Any

from maicoin_max.client import Client
from maicoin_max.dto.market import Candlestick

from dto.market_dto import CandlestickDto
from exchange.maicoin_max import gen_request_client, max_utils
from infra.enums import CandlestickInterval
from service.market_client_sevice import MarketClientService


def _clac_limit_timestamp(period: int, startTime: datetime = None, endTime: datetime = None,
                          org_limit: int = None) -> (int, int):
    """
    :param period:
    :param startTime:
    :param endTime:
    :param org_limit:
    :return: 1 : limit , 2: timestamp
    """
    p_seconds = period * 60
    if org_limit is None:
        org_limit = 1
    if startTime is None and endTime is None:
        return org_limit, int(datetime.now(tz=timezone.utc).timestamp()) - (p_seconds * org_limit)

    if startTime is None:
        return org_limit, int(endTime.timestamp())  - (p_seconds * org_limit)
    if endTime is None:
        endTime = datetime.now(tz=timezone.utc)
    diff = endTime - startTime
    diff_limit = (diff.total_seconds() / 60) / period
    final_limit = min(org_limit, diff_limit)
    return final_limit, int(startTime.timestamp()) + (p_seconds * final_limit)


def _candlestick_interval_minute(interval: CandlestickInterval) -> int:
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


class MaxMarketClientService(MarketClientService):

    def __init__(self, **kwargs):
        super(MaxMarketClientService, self).__init__(**kwargs)
        self.client: Client = gen_request_client()

    def get_candlestick_data(self, prd_name: str, interval: CandlestickInterval, startTime: datetime = None,
                             endTime: datetime = None, limit: int = None) -> List[CandlestickDto]:
        period = _candlestick_interval_minute(interval)
        (limit, timestamp) = _clac_limit_timestamp(period=period, startTime=startTime, endTime=endTime, org_limit=limit)
        k_result: List[Candlestick] = self.client.get_public_k_line(pair=max_utils.unfix_symbol(prd_name), limit=limit,
                                                                    timestamp=timestamp, period=period)
        return [max_utils.convert_candlestick_dto(kd) for kd in k_result]

    def get_exchange_info(self) -> Any:
        return self.client.get_exchange_information()


def get_impl_clazz() -> MaxMarketClientService:
    return MaxMarketClientService
