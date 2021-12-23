from binance_f import RequestClient
from sqlalchemy.orm import Session

from exchange.binance import gen_request_client
from service.order_builder import LimitOrderBuilder


class BitfinexLimitOrderBuilder(LimitOrderBuilder):

    def __init__(self, exchange_name: str, session: Session):
        super(BitfinexLimitOrderBuilder, self).__init__(exchange_name, session)
        self.client: RequestClient = gen_request_client()

    # def post_one(self, pq: PriceQty) -> OrderDto:
    #     price_str = str(self.productDao.fix_precision_price(self.product, pq.price))
    #
    #     p_amt: float = self.productDao.fix_precision_amt(self.product, pq.quantity)
    #     if p_amt == 0:
    #         return None
    #     quantity_str = str(p_amt)
    #
    #     ans = self.client.post_order(price=price_str,
    #                                  side=self.get_order_side(),
    #                                  symbol=binance_utils.fix_usdt_symbol(self.dto.symbol),
    #                                  timeInForce=TimeInForce.GTC,
    #                                  ordertype=OrderType.LIMIT,
    #                                  workingType=WorkingType.CONTRACT_PRICE,
    #                                  positionSide=self.dto.positionSide,
    #                                  # activationPrice=None,
    #                                  # closePosition=False,
    #                                  quantity=quantity_str,
    #                                  newClientOrderId=comm_utils.get_order_cid(tags=self.dto.tags)
    #                                  )
    #     return binance_utils.convert_order_dto(ans)


def get_impl_clazz() -> BitfinexLimitOrderBuilder:
    return BitfinexLimitOrderBuilder
