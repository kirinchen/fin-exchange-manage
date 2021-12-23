from typing import List

from sqlalchemy.orm import Session

from binance_f import RequestClient
from binance_f.model import Trade
from dto.trade_dto import TradeDto
from exchange.binance import gen_request_client, binance_utils
from service.trade_client_service import TradeClientService


class BitfinexTradeClientService(TradeClientService):

    def __init__(self, exchange_name: str, session: Session):
        super(BitfinexTradeClientService, self).__init__(exchange_name, session)
        self.client: RequestClient = gen_request_client()

    def fetch_recent_list(self, symbol: str, limit: int) -> List[TradeDto]:
        org_list: List[Trade] = self.client.get_recent_trades_list(symbol=binance_utils.fix_usdt_symbol(symbol),
                                                                   limit=limit)
        return [binance_utils.convert_trade_dto(ot) for ot in org_list]


def get_impl_clazz() -> BitfinexTradeClientService:
    return BitfinexTradeClientService
