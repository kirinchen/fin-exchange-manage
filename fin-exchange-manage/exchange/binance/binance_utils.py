from datetime import datetime
from enum import Enum

import pytz
from binance_f.exception.binanceapiexception import BinanceApiException
from binance_f.model import Order, Trade, Position, Candlestick

from dto.market_dto import CandlestickDto
from dto.order_dto import OrderDto
from dto.position_dto import PositionDto
from dto.trade_dto import TradeDto
from model import Product
from service.order_client_service import OrderClientService


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
