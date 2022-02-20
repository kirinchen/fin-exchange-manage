from datetime import datetime
from typing import List, Any

from binance_f import RequestClient
from binance_f.model import Candlestick

from exchange.binance import gen_request_client, binance_utils
from infra.enums import CandlestickInterval
from service.market_client_sevice import MarketClientService


class CandlestickDto:
    pass


class BinanceMarketClientService(MarketClientService):

    def __init__(self, **kwargs):
        super(BinanceMarketClientService, self).__init__(**kwargs)
        self.client: RequestClient = gen_request_client()

    def get_candlestick_data(self, prd_name: str, interval: CandlestickInterval, startTime: datetime = None,
                             endTime: datetime = None, limit: int = None) -> List[CandlestickDto]:
        start_int = int(startTime.timestamp() * 1000) if startTime else None
        end_int = int(endTime.timestamp() * 1000) if endTime else None
        result: List[Candlestick] = self.client.get_candlestick_data(symbol=binance_utils.fix_usdt_symbol(prd_name),
                                                                     interval=interval,
                                                                     startTime=start_int,
                                                                     endTime=end_int, limit=limit)
        return [binance_utils.convert_candlestick_dto(r) for r in result]

    def get_exchange_info(self) -> Any:
        return self.client.get_exchange_information()


def get_impl_clazz() -> BinanceMarketClientService:
    return BinanceMarketClientService
