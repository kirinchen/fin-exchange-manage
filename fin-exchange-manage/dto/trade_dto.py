from datetime import datetime
from typing import List, Dict

from utils import time_utils


class TradeDto:

    def __init__(self, price: float, qty: float, quoteQty: float, time: datetime, isBuyerMaker: bool, **kwargs):
        self.price: float = price
        self.qty: float = qty
        self.quoteQty: float = quoteQty
        self.time: datetime = time
        self.isBuyerMaker: bool = isBuyerMaker


class TradeRange:
    def __init__(self):
        self.avgPrice = 0
        self.totalAmount = 0
        self.lastPrice = 0
        self.lastAt: datetime = None
        self.highPrice = 0
        self.highPriceAt: datetime = None
        self.lowPrice = 0
        self.lowPriceAt: datetime = None
        self.highAmount = 0
        self.highAmountAt: datetime = None
        self.trades: List[TradeDto] = list()
        self.timeValMap: Dict[str, float] = None

    def subtotal(self, time_maped: bool = False):
        try:
            amt = 0
            sup = 0
            for t in self.trades:
                amt += t.qty
                sup += t.qty * t.price
            self.totalAmount = amt
            self.avgPrice = sup / self.totalAmount
            hpe = self.calc_max('price')
            self.highPrice = hpe.price
            self.highPriceAt = hpe.time
            lpe = self.calc_min('price')
            self.lowPrice = lpe.price
            self.lowPriceAt = lpe.time
            hae = self.calc_max('qty')
            self.highAmount = hae.qty
            self.highAmountAt = hae.time()
            le = self.calc_max('time')
            self.lastPrice = le.price
            self.lastAt = le.time

            if not time_maped:
                return
            self.timeValMap = gen_time_val_map(self)

        except Exception as e:  # work on python 3.x
            print(e)

    def get_first(self) -> TradeDto:
        return self.calc_min('time')

    def calc_max(self, f: str) -> TradeDto:
        return max(self.trades, key=lambda x: getattr(x.get_data(), f))

    def calc_min(self, f: str) -> TradeDto:
        return min(self.trades, key=lambda x: getattr(x.get_data(), f))


def gen_time_val_map(ts: TradeRange) -> Dict[str, float]:
    ans: Dict[str, float] = dict()
    for t in ts.trades:
        ans[time_utils.to_time_utc_iso(t.time)] = t.price()
    return ans
