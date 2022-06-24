import math
from typing import List

from bfxapi import Wallet
from sqlalchemy.orm import Session

from dto.wallet_dto import WalletDto
from exchange.bitfinex import gen_request_client, bitfinex_utils
from infra.enums import PayloadExKey
from service.wallet_client_service import WalletClientService
from utils import comm_utils

LEND_MIN_AMOUNT = 151


class LendAmtRateSet:

    def __init__(self, rate: float, day: int, amount: float):
        self.rate: float = rate
        self.day: int = day
        self.amount: float = amount


class LendPrams:

    def __init__(self, rowAmount: float, minMaxDiffRate: float,  middleWeight: float, **kwargs):
        self.rowAmount: float = rowAmount
        self.minMaxDiffRate:float = minMaxDiffRate
        self.middleWeight: float = middleWeight


class BitfinexWalletClientService(WalletClientService):

    def __init__(self, **kwargs):
        super(BitfinexWalletClientService, self).__init__(**kwargs)
        (self.client, self.expandClient) = gen_request_client(PayloadExKey.exchange_account.get_val(self.payload))

    def list_all(self) -> List[WalletDto]:
        result: List[Wallet] = bitfinex_utils.call(self.client.rest.get_wallets())
        return [bitfinex_utils.convert_wallet_dto(w) for w in result]

    def cancel_lend_all(self, w: WalletDto):
        bitfinex_utils.call(self.expandClient.cancel_funding_all(w.symbol))

    def lend_one(self, w: WalletDto, **kwargs) -> object:
        lend_prams = LendPrams(**kwargs)
        if w.balance_available < LEND_MIN_AMOUNT:
            return f'no enough {comm_utils.to_dict(w)}'
        lend_amt_rate_set = self.gen_lend_price_set(w, lend_prams)
        ans = list()
        for amt_rate in lend_amt_rate_set:
            r = bitfinex_utils.call(
                self.client.rest.submit_funding_offer(symbol=f'f{w.symbol}', amount=amt_rate.amount, rate=amt_rate.rate,
                                                      period=amt_rate.day))
            ans.append(r)
        return ans

    def gen_lend_price_set(self, w: WalletDto, lp: LendPrams) -> List[LendAmtRateSet]:
        result: List[list] = bitfinex_utils.call(
            self.client.rest.get_public_books(symbol='f' + w.symbol, precision='P1', length=100))
        rate_list: List[float] = [a[0] for a in result]
        max_rate = max(rate_list)
        min_rate = min(rate_list)

        middle_rate = (max_rate + min_rate) * lp.middleWeight

        dr = (max_rate - middle_rate) * lp.minMaxDiffRate

        cusd = w.balance_available
        cusd = cusd - LEND_MIN_AMOUNT

        spcount = math.floor(cusd / lp.rowAmount)

        rp = dr / spcount

        batchList: List[LendAmtRateSet] = list()

        for i in range(spcount):
            batchList.append(LendAmtRateSet(rate=middle_rate + ((i + 1) * rp), day=i + 2, amount=lp.rowAmount))

        lasta = cusd + LEND_MIN_AMOUNT - (spcount * lp.rowAmount)
        batchList.append(LendAmtRateSet(rate=max_rate, day=5, amount=lasta))
        return batchList


def get_impl_clazz() -> BitfinexWalletClientService:
    return BitfinexWalletClientService
