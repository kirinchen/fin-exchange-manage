from binance_f.model import Order
from dto.order_dto import OrderDto


def fix_usdt_symbol(symbol: str) -> str:
    return f'{symbol}USDT'

def convert_order_dto(b_order:Order)->OrderDto:
    ans = OrderDto(**b_order.__dict__)
    ans.symbol = b_order.symbol.replace('USDT','')
    return ans
