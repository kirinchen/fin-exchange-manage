from typing import List

from binance_f import RequestClient
from binance_f.model import Trade

from dto.trade_dto import TradeDto
from exchange.binance import gen_request_client, binance_utils
from service.trade_client_service import TradeClientService


class BinanceTradeClientService(TradeClientService):

    def __init__(self, **kwargs):
        super(BinanceTradeClientService, self).__init__(**kwargs)
        self.client: RequestClient = gen_request_client()

    def fetch_recent_list(self, prd_name: str, limit: int) -> List[TradeDto]:
        org_list: List[Trade] = self.client.get_recent_trades_list(symbol=binance_utils.fix_usdt_symbol(prd_name),
                                                                   limit=limit)
        return [binance_utils.convert_trade_dto(ot) for ot in org_list]


def get_impl_clazz() -> BinanceTradeClientService:
    return BinanceTradeClientService
