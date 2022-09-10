import asyncio
from datetime import datetime
from typing import Any, List

from bfxapi import Wallet

from dto.market_dto import CandlestickDto
from dto.wallet_dto import WalletDto


def convert_wallet_dto(w: Wallet) -> WalletDto:
    ans = WalletDto(**w.__dict__)
    ans.symbol = w.currency
    ans.wallet_type = w.type
    ans.uid = w.key
    return ans


def convert_candlestick_dto(l: list) -> CandlestickDto:
    ans = CandlestickDto()
    ans.closeAt = datetime.fromtimestamp(l[0]/1000)
    ans.open = l[1]
    ans.close = l[2]
    ans.high = l[3]
    ans.low = l[4]
    ans.volume = l[5]
    return ans


def call(coroutine) -> Any:
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(coroutine)
