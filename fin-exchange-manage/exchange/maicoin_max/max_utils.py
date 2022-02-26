from datetime import datetime
from typing import List

import pytz
from maicoin_max.client import Client
from maicoin_max.dto.order import Order
from maicoin_max.dto.position import Position
from maicoin_max.dto.wallet import Wallet

from dto.account_dto import AccountDto
from dto.order_dto import OrderDto
from dto.wallet_dto import WalletDto
from infra.enums import PositionSide, OrderStatus, OrderSide, OrderType


def fix_usdt_symbol(symbol: str) -> str:
    return f'{symbol}usdt'


def trim_usdt_symbol(symbol: str) -> str:
    return symbol.replace('usdt', '')


def convert_account_dto(client: Client, positions: List[Position]) -> AccountDto:
    raise NotImplementedError('convert_account_dto')  # TODO


def convert_order_dto(o: Order) -> OrderDto:
    ans = OrderDto(
        clientOrderId=o.client_oid
        , cumQuote=None
        , executedQty=float(o.executed_volume) if o.executed_volume else -1
        , orderId=o.id
        , origQty=float(o.volume) if o.volume else -1
        , price=float(o.price) if o.price else -1
        , side=convert_order_side(o.side)
        , status=convert_status(o.state)
        , stopPrice=float(o.stop_price) if o.stop_price else -1
        , symbol=o.market
        , type=convert_order_type(o.ord_type)
        , updateTime=o.updated_at_in_ms
        , avgPrice=float(o.avg_price) if o.avg_price else -1
        , origType=convert_order_type(o.ord_type)
        , positionSide=PositionSide.LONG
        , activatePrice=float(o.price) if o.price else -1
        , priceRate=None
        , closePosition=None
        , updateAt=datetime.fromtimestamp(o.updated_at_in_ms / 1000, pytz.utc).isoformat()
    )
    return ans


def convert_order_type(t: str) -> OrderType:
    return {
        'limit': OrderType.LIMIT,
        'market': OrderType.MARKET,
        'stop_limit': OrderType.STOP_MARKET,
        'stop_market': OrderType.STOP_MARKET
    }.get(t, t)


def convert_order_side(s: str) -> OrderSide:
    return {
        'buy': OrderSide.BUY,
        'sell': OrderSide.SELL
    }.get(s)


def convert_status(state: str) -> OrderStatus:
    return {
        'cancel': OrderStatus.CANCELED,
        'wait': OrderStatus.NEW,
        'done': OrderStatus.FILLED,
        'finalizing': OrderStatus.PARTIALLY_FILLED,
        'failed': OrderStatus.REJECTED,
        'convert': OrderStatus.NEW
    }.get(state)


def convert_wallet(wallet: Wallet) -> WalletDto:
    ans = WalletDto()
    ans.wallet_type = wallet.type
    ans.symbol = wallet.currency
    ans.uid = wallet.type + wallet.currency
    ans.balance = wallet.balance
    ans.balance_available = wallet.balance - wallet.locked
    return ans
