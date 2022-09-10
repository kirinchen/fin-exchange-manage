import math
from datetime import datetime
from enum import Enum

import pytz
from binance_f.exception.binanceapiexception import BinanceApiException
from binance_f.model import Order, Trade, Position, Candlestick
from binance_f.model.exchangeinformation import Symbol

from dto.market_dto import CandlestickDto
from dto.order_dto import OrderDto
from dto.position_dto import PositionDto
from dto.trade_dto import TradeDto
from model import Product
from service.order_client_service import OrderClientService
from utils import reflection_util


def fix_usdt_symbol(symbol: str) -> str:
    return f'{symbol}USDT'


def trim_usdt_symbol(symbol: str) -> str:
    return symbol.replace('USDT', '')


def convert_order_dto(b_order: Order) -> OrderDto:
    ans = OrderDto(**b_order.__dict__)
    ans.symbol = trim_usdt_symbol(b_order.symbol)
    ans.updateAt = datetime.fromtimestamp(ans.updateTime / 1000, pytz.utc).isoformat()
    return ans


def convert_trade_dto(b_trade: Trade) -> TradeDto:
    t_dict = b_trade.__dict__
    time_time = datetime.fromtimestamp(b_trade.time / 1000)
    t_dict['time'] = time_time
    return TradeDto(**t_dict)


def convert_position_dto(b_position: Position) -> PositionDto:
    ans = PositionDto(**b_position.__dict__)
    ans.symbol = trim_usdt_symbol(b_position.symbol)
    return ans


def convert_candlestick_dto(ct: Candlestick) -> CandlestickDto:
    t_dict = ct.__dict__
    oc_dt = (ct.closeTime - ct.openTime) / 3

    op_time = datetime.fromtimestamp(ct.openTime / 1000)
    cl_time = datetime.fromtimestamp(ct.closeTime / 1000)
    t_dict['openAt'] = op_time
    t_dict['closeAt'] = cl_time
    t_dict['highAt'] = None
    t_dict['lowAt'] = None
    return CandlestickDto(**t_dict)


class ErrorCode(Enum):
    LIMIT_PRICE_CAN_NOT_BE_HIGHER = 4016
    ORDER_WOULD_IMMEDIATELY_TRIGGER = 2021


def is_exception(code: ErrorCode, ex: BinanceApiException) -> bool:
    code_str = f' -{code.value}'
    msg = ex.error_message
    return code_str in msg


class FilterInfo:

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            if reflection_util.has_key(self, k):
                reflection_util.setval(self, k, float(v))


class PriceInfo(FilterInfo):

    def __init__(self, **kwargs):
        self.minPrice: float = -1
        self.maxPrice: float = -1
        self.tickSize: float = -1
        super(PriceInfo, self).__init__(**kwargs)


class AmtInfo(FilterInfo):

    def __init__(self, **kwargs):
        self.stepSize: float = -1
        self.maxQty: float = -1
        self.minQty: float = -1
        super(AmtInfo, self).__init__(**kwargs)


_PRECISION = 1000000.0


class SymbolHelper:

    def __init__(self, symbol: Symbol):
        self.symbol: Symbol = symbol

    def _get_filter(self, filterType: str) -> dict:
        return [f for f in self.symbol.filters if f.get('filterType') == filterType][0]

    def get_price_info(self) -> PriceInfo:
        info = self._get_filter('PRICE_FILTER')
        ans = PriceInfo(**info)
        return ans

    def get_amt_info(self) -> AmtInfo:
        info = self._get_filter('MARKET_LOT_SIZE')
        ans = AmtInfo(**info)
        return ans

    def fix_precision_price(self, price: float) -> float:
        pi = self.get_price_info()
        count = int(math.floor(price / pi.tickSize))
        ans = math.floor(count * pi.tickSize * _PRECISION) / _PRECISION
        return ans

    def fix_precision_amt(self, amt: float, to_int_func=math.floor) -> float:
        a = self.get_amt_info()
        count = to_int_func(amt / a.stepSize)
        ans = math.floor(count * a.stepSize * _PRECISION) / _PRECISION
        return ans

    def get_min_amt(self) -> float:
        a = self.get_amt_info()
        return a.minQty


def convert_symbol_helper(product: Product) -> SymbolHelper:
    cfg = product.get_config()
    sbl: Symbol = reflection_util.merge(cfg, Symbol())
    return SymbolHelper(sbl)
