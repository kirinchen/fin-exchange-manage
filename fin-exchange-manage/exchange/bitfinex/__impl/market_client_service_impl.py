from datetime import datetime, timedelta
from typing import List, Any

from dto.market_dto import CandlestickDto
from exchange.bitfinex import gen_request_client, bitfinex_utils
from infra.enums import CandlestickInterval, PayloadExKey
from service.market_client_sevice import MarketClientService


class BitfinexMarketClientService(MarketClientService):

    def __init__(self, **kwargs):
        super(BitfinexMarketClientService, self).__init__(**kwargs)
        (self.client, self.expandClient) = gen_request_client(PayloadExKey.exchange_account.get_val(self.payload))

    def get_candlestick_data(self, prd_name: str, interval: CandlestickInterval, startTime: datetime = None,
                             endTime: datetime = None, limit: int = None) -> List[CandlestickDto]:
        start_int = str(int(startTime.timestamp() * 1000)) if startTime else None
        end_int = str(int(endTime.timestamp() * 1000)) if endTime else None
        org_list: List[list] = bitfinex_utils.call(
            self.client.rest.get_public_candles(symbol=prd_name, tf=interval, start=start_int, end=end_int,
                                                limit=limit))

        return [bitfinex_utils.convert_candlestick_dto(o) for o in org_list]

    def get_exchange_info(self) -> Any:
        raise NotImplementedError("get_exchange_info")


def get_impl_clazz() -> BitfinexMarketClientService:
    return BitfinexMarketClientService
