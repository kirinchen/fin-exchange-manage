from binance_f import RequestClient
from binance_f.model import TimeInForce, OrderType, WorkingType
from dto.order_dto import OrderDto
from exchange.binance import gen_request_client
from service.order_builder import LimitOrderBuilder, PriceQty
from utils import comm_utils


class BinanceLimitOrderBuilder(LimitOrderBuilder):

    def __init__(self, exchange_name: str):
        super(BinanceLimitOrderBuilder, self).__init__(exchange_name)
        self.client: RequestClient = gen_request_client()

    def post_one(self, pq: PriceQty) -> OrderDto:
        price_str = str(self.dto.get_symbol().fix_precision_price(pq.price))

        p_amt: float = self.dto.get_symbol().fix_precision_amt(pq.quantity)
        if p_amt == 0:
            return None
        quantity_str = str(p_amt)

        return self.client.post_order(price=price_str,
                                      side=self.get_order_side(),
                                      symbol=self.dto.get_symbol().gen_with_usdt(),
                                      timeInForce=TimeInForce.GTC,
                                      ordertype=OrderType.LIMIT,
                                      workingType=WorkingType.CONTRACT_PRICE,
                                      positionSide=self.dto.positionSide,
                                      # activationPrice=None,
                                      # closePosition=False,
                                      quantity=quantity_str,
                                      newClientOrderId=comm_utils.get_order_cid(tags=self.dto.tags)
                                      )
