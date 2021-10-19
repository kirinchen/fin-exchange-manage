from binance_f import RequestClient
from dto.order_dto import OrderDto
from exchange.binance import gen_request_client
from service.order_builder import LimitOrderBuilder, PriceQty


class BinanceLimitOrderBuilder(LimitOrderBuilder):

    def __init__(self, exchange_name: str):
        super(BinanceLimitOrderBuilder, self).__init__(exchange_name)
        self.client: RequestClient = gen_request_client()

    def post_one(self, pq: PriceQty) -> OrderDto:
        pass
