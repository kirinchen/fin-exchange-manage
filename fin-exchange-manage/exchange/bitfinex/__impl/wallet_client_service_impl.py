import asyncio
import math
from typing import List

from bfxapi import Client, Wallet
from binance_f import RequestClient
from sqlalchemy.orm import Session

from dto.wallet_dto import WalletDto
from exchange.bitfinex import gen_request_client, bitfinex_utils
from service.wallet_client_service import WalletClientService
from utils import comm_utils

LEND_MIN_AMOUNT = 50


class LendPriceSet:

    def __init__(self, rate: float, day: int, amount: float):
        self.rate: float = rate
        self.day: int = day
        self.amount: float = amount


class LendPrams:

    def __init__(self, rowAmount: float, **kwargs):
        self.rowAmount: float = rowAmount


class BitfinexWalletClientService(WalletClientService):

    def __init__(self, exchange_name: str, session: Session = None):
        super(BitfinexWalletClientService, self).__init__(exchange_name, session)
        self.client: Client = gen_request_client()

    def list_all(self) -> List[WalletDto]:
        # loop = asyncio.get_event_loop()
        # coroutine = self.client.rest.get_wallets()
        # result: List[Wallet] = loop.run_until_complete(coroutine)
        result: List[Wallet] = bitfinex_utils.call(self.client.rest.get_wallets())
        return [bitfinex_utils.convert_wallet_dto(w) for w in result]

    def lend_one(self, w: WalletDto, **kwargs) -> object:
        lend_prams = LendPrams(**kwargs)
        if w.balance_available < LEND_MIN_AMOUNT:
            return f'no enough {comm_utils.to_dict(w)}'
        lend_price_set = self.gen_lend_price_set(w, lend_prams)
        return comm_utils.to_dict(lend_price_set)

    def gen_lend_price_set(self, w: WalletDto, lp: LendPrams) -> List[LendPriceSet]:
        result: List[list] = bitfinex_utils.call(
            self.client.rest.get_public_books(symbol='f' + w.symbol, precision='P1', length=100))
        rate_list: List[float] = [a[0] for a in result]
        mx = max(rate_list)
        mn = min(rate_list)
        mn *= 1.02
        mx *= 1.01
        mn = (mx + mn) * 0.23

        dr = mx - mn

        cusd = w.balance_available
        cusd = cusd - LEND_MIN_AMOUNT

        spcount = math.floor(cusd / lp.rowAmount)

        rp = dr / spcount

        batchList: List[LendPriceSet] = list()

        for i in range(spcount):
            batchList.append(LendPriceSet(rate=mn + ((i + 1) * rp), day=i + 2, amount=lp.rowAmount))

        lasta = cusd + LEND_MIN_AMOUNT - (spcount * lp.rowAmount)
        batchList.append(LendPriceSet(rate=mx, day=5, amount=lasta))
        return batchList


def get_impl_clazz() -> BitfinexWalletClientService:
    return BitfinexWalletClientService
