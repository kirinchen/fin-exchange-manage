import math
from typing import List

from bfxapi import Wallet

from dto.market_dto import CandlestickDto
from dto.wallet_dto import WalletDto
from exchange.bitfinex import gen_request_client, bitfinex_utils
from infra.enums import PayloadExKey, CandlestickInterval
from service.market_client_sevice import MarketClientService
from service.wallet_client_service import WalletClientService
from utils import comm_utils

# LEND_MIN_AMOUNT = 160


class LendAmtRateSet:

    def __init__(self, rate: float, day: int, amount: float):
        self.rate: float = rate
        self.day: int = day
        self.amount: float = amount


class LendPrams:

    def __init__(self, rowAmount: float, rangeRate: float, maxRateMultiple: float, **kwargs):
        self.rowAmount: float = rowAmount
        self.maxRateMultiple: float = maxRateMultiple
        self.rangeRate: float = rangeRate


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
        if w.balance_available < lend_prams.rowAmount:
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
        mService: MarketClientService = self.get_ex_obj(MarketClientService)
        # result: List[list] = bitfinex_utils.call(
        #     self.client.rest.get_public_books(symbol='f' + w.symbol, precision='P1', length=100))
        p2_candle = mService.get_candlestick_data(prd_name='f' + w.symbol + ':p2', limit=1
                                                  , interval='1D')[0]
        p30_candle = mService.get_candlestick_data(prd_name='f' + w.symbol + ':p30', limit=1
                                                   , interval='1D')[0]

        max_rate = avg_val([p30_candle.high, p2_candle.high]) * lp.maxRateMultiple
        min_rate = avg_val([
            p30_candle.low, p2_candle.low
        ])

        dr = (max_rate - min_rate) * lp.rangeRate
        dr = abs(dr)
        cusd = w.balance_available
        cusd = cusd - lp.rowAmount

        spcount = math.floor(cusd / lp.rowAmount)

        rp = dr / spcount if spcount > 0 else dr

        batchList: List[LendAmtRateSet] = list()

        for i in range(spcount):
            batchList.append(LendAmtRateSet(rate=max_rate - (i * rp), day=(spcount - i) + 2, amount=lp.rowAmount))

        lasta = cusd + lp.rowAmount - (spcount * lp.rowAmount)
        batchList.append(LendAmtRateSet(rate=max_rate, day=5, amount=lasta))
        return batchList


def avg_val(fl: List[float]) -> float:
    _sum = sum(fl)
    return _sum / len(fl)


def get_impl_clazz() -> BitfinexWalletClientService:
    return BitfinexWalletClientService
