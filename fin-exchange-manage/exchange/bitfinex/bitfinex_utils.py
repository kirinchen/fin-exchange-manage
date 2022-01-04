import asyncio
from typing import Any

from bfxapi import Wallet

from dto.wallet_dto import WalletDto


def convert_wallet_dto(w: Wallet) -> WalletDto:
    ans = WalletDto(**w.__dict__)
    ans.symbol = w.currency
    ans.wallet_type = w.type
    ans.uid = w.key
    return ans


def call(coroutine) -> Any:
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(coroutine)
