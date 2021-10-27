from datetime import datetime

from binance_f.model import Order, Trade, Position
from dto.order_dto import OrderDto
from dto.position_dto import PositionDto
from dto.trade_dto import TradeDto


def fix_usdt_symbol(symbol: str) -> str:
    return f'{symbol}USDT'


def trim_usdt_symbol(symbol: str) -> str:
    return symbol.replace('USDT', '')


def convert_order_dto(b_order: Order) -> OrderDto:
    ans = OrderDto(**b_order.__dict__)
    ans.symbol = trim_usdt_symbol(b_order.symbol)
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
