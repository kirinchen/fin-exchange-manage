from binance_f import RequestClient
from binance_f.model import TimeInForce, OrderType, WorkingType
from dto.order_dto import OrderDto
from exchange.binance import gen_request_client
from model import Product
from model.init_data import init_item
from service.order_builder import LimitOrderBuilder, PriceQty
from utils import comm_utils


class BinanceLimitOrderBuilder(LimitOrderBuilder):

    def __init__(self, exchange_name: str):
        super(BinanceLimitOrderBuilder, self).__init__(exchange_name)
        self.client: RequestClient = gen_request_client()

    def post_one(self, pq: PriceQty) -> OrderDto:
        product_entity: Product = self.exchangeProductDao.get_by_item_symbol(self.dto.symbol,
                                                                             init_item.get_instance().usdt.symbol)
        price_str = str(self.exchangeProductDao.fix_precision_price(product_entity.price))

        p_amt: float = self.exchangeProductDao.fix_precision_amt(product_entity.quantity)
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


def get_impl_clazz() -> BinanceLimitOrderBuilder:
    return BinanceLimitOrderBuilder
