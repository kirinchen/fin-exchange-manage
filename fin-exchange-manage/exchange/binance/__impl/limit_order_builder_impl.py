from sqlalchemy.orm import Session

from binance_f import RequestClient
from binance_f.model import TimeInForce, OrderType, WorkingType
from dto.order_dto import OrderDto
from exchange.binance import gen_request_client, binance_utils
from model.init_data import init_item
from service.order_builder import LimitOrderBuilder, PriceQty
from utils import comm_utils


class BinanceLimitOrderBuilder(LimitOrderBuilder):

    def __init__(self, exchange_name: str, session: Session):
        super(BinanceLimitOrderBuilder, self).__init__(exchange_name, session)
        self.client: RequestClient = gen_request_client()

    def post_one(self, pq: PriceQty) -> OrderDto:
        price_str = str(self.productDao.fix_precision_price(self.product, pq.price))

        p_amt: float = self.productDao.fix_precision_amt(self.product, pq.quantity)
        if p_amt == 0:
            return None
        quantity_str = str(p_amt)

        return self.client.post_order(price=price_str,
                                      side=self.get_order_side(),
                                      symbol=binance_utils.fix_usdt_symbol(self.dto.symbol),
                                      timeInForce=TimeInForce.GTC,
                                      ordertype=OrderType.LIMIT,
                                      workingType=WorkingType.CONTRACT_PRICE,
                                      positionSide=self.dto.positionSide,
                                      # activationPrice=None,
                                      # closePosition=False,
                                      quantity=quantity_str,
                                      newClientOrderId=comm_utils.get_order_cid(tags=self.dto.tags)
                                      )


def get_impl_clazz() -> BinanceLimitOrderBuilder:
    return BinanceLimitOrderBuilder
