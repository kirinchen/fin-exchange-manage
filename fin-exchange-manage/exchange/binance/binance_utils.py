from datetime import datetime

from binance_f.model import Order, Trade
from dto.order_dto import OrderDto
from dto.trade_dto import TradeDto


def fix_usdt_symbol(symbol: str) -> str:
    return f'{symbol}USDT'


def convert_order_dto(b_order: Order) -> OrderDto:
    ans = OrderDto(**b_order.__dict__)
    ans.symbol = b_order.symbol.replace('USDT', '')
    return ans


def convert_trade_dto(b_trade: Trade) -> TradeDto:
    t_dict = b_trade.__dict__
    time_time = datetime.fromtimestamp(b_trade.time / 1000)
    t_dict['time'] = time_time
    return TradeDto(**t_dict)
