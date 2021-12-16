from binance_f import RequestClient
from sqlalchemy.orm import Session

from exchange.binance import gen_request_client, binance_utils
from infra.enums import CandlestickInterval
from service.market_client_sevice import MarketClientService


class BinanceMarketClientService(MarketClientService):

    def __init__(self, exchange_name: str, session: Session = None):
        super(BinanceMarketClientService, self).__init__(exchange_name, session)
        self.client: RequestClient = gen_request_client()

    def get_candlestick_data(self, prd_name:str, interval: CandlestickInterval, startTime: int = None,
                             endTime: int = None, limit: int = None) -> any:
        return self.client.get_candlestick_data(symbol=binance_utils.fix_usdt_symbol(prd_name), interval=interval,
                                                startTime=startTime,
                                                endTime=endTime, limit=limit)


def get_impl_clazz() -> BinanceMarketClientService:
    return BinanceMarketClientService
