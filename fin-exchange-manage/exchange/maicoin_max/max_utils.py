from datetime import datetime
from typing import List

from dto.account_dto import AccountDto
from dto.order_dto import OrderDto
from dto.position_dto import PositionDto
from dto.trade_dto import TradeDto
from max_exchange_api_python3.max.client import Client
from max_exchange_api_python3.max.dto.position import Position


def fix_usdt_symbol(symbol: str) -> str:
    return f'{symbol}usdt'


def trim_usdt_symbol(symbol: str) -> str:
    return symbol.replace('usdt', '')


def convert_account_dto(client: Client, positions: List[Position]) -> AccountDto:
    raise NotImplementedError('convert_account_dto')  # TODO
