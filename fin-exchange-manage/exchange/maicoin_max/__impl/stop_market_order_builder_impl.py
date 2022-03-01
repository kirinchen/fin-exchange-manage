from sqlalchemy.orm import Session

from binance_f import RequestClient
from binance_f.model import TimeInForce, OrderType, WorkingType
from dto.order_dto import OrderDto
from exchange.binance import gen_request_client, binance_utils
from service.order_builder import TakeProfitOrderBuilder, PriceQty, StopMarketOrderBuilder
from utils import comm_utils


class MaxStopMarketOrderBuilder(StopMarketOrderBuilder):
    pass


def get_impl_clazz() -> MaxStopMarketOrderBuilder:
    return MaxStopMarketOrderBuilder
