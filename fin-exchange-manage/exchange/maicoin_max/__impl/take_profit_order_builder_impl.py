from sqlalchemy.orm import Session

from binance_f import RequestClient
from binance_f.model import TimeInForce, OrderType, WorkingType
from dto.order_dto import OrderDto
from exchange.binance import gen_request_client, binance_utils
from service.order_builder import TakeProfitOrderBuilder, PriceQty
from utils import comm_utils


class BinanceTakeProfitOrderBuilder(TakeProfitOrderBuilder):

    def __init__(self, exchange_name: str, session: Session):
        super(BinanceTakeProfitOrderBuilder, self).__init__(exchange_name, session)
        self.client: RequestClient = gen_request_client()

    def post_one(self, pq: PriceQty) -> OrderDto:
        price_str = str(self.productDao.fix_precision_price(self.product, pq.price))
        p_amt: float = self.productDao.fix_precision_amt(self.product, pq.quantity)
        if p_amt == 0:
            return None
        quantity_str = str(p_amt)
        side = self.get_order_side()
        result = self.client.post_order(
            side=side,
            symbol=binance_utils.fix_usdt_symbol(self.dto.symbol),
            timeInForce=TimeInForce.GTC,
            ordertype=OrderType.TAKE_PROFIT_MARKET,
            workingType=WorkingType.CONTRACT_PRICE,
            positionSide=self.dto.positionSide,
            stopPrice=price_str,
            quantity=quantity_str,
            newClientOrderId=comm_utils.get_order_cid(self.dto.tags)
        )
        return binance_utils.convert_order_dto(result)


def get_impl_clazz() -> BinanceTakeProfitOrderBuilder:
    return BinanceTakeProfitOrderBuilder