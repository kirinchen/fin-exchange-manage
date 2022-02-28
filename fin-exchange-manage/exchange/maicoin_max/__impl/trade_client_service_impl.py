from datetime import datetime, timezone
from typing import List

from maicoin_max.client import Client
from maicoin_max.dto.market import Trade

from dto.trade_dto import TradeDto
from exchange.maicoin_max import gen_request_client, max_utils
from service.trade_client_service import TradeClientService


class MaxTradeClientService(TradeClientService):

    def __init__(self, **kwargs):
        super(MaxTradeClientService, self).__init__(**kwargs)
        self.client: Client = gen_request_client()

    def fetch_recent_list(self, prd_name: str, limit: int) -> List[TradeDto]:
        org_list:List[Trade] = self.client.get_public_recent_trades(pair=max_utils.unfix_symbol(prd_name), limit=limit)
        return [max_utils.convert_trade(t) for t in org_list]
        # return [binance_utils.convert_trade_dto(ot) for ot in org_list]


def get_impl_clazz() -> MaxTradeClientService:
    return MaxTradeClientService
