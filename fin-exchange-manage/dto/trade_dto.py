from datetime import datetime
from typing import List, Dict


class Trade:

    def __init__(self, price: float, qty: float, quoteQty: float, time: int, isBuyerMaker: bool, **kwargs):
        self.price: float = price
        self.qty: float = qty
        self.quoteQty: float = quoteQty
        self.time: int = time
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
        self.trades: List[Trade] = list()
        self.timeValMap: Dict[str, float] = None

    def subtotal(self, time_maped: bool = False):
        try:
            amt = 0
            sup = 0
            for t in self.trades:
                amt += t.qty()
                sup += t.qty() * t.price()
            self.totalAmount = amt
            self.avgPrice = sup / self.totalAmount
            hpe = self.clac_max('price')
            self.highPrice = hpe.price()
            self.highPriceAt = datetime.fromtimestamp(hpe.time() / 1000)
            lpe = self.clac_min('price')
            self.lowPrice = lpe.price()
            self.lowPriceAt = datetime.fromtimestamp(lpe.time() / 1000)
            hae = self.clac_max('qty')
            self.highAmount = hae.qty()
            self.highAmountAt = datetime.fromtimestamp(hae.time() / 1000)
            le = self.clac_max('time')
            self.lastPrice = le.price()
            self.lastAt = datetime.fromtimestamp(le.time() / 1000)

            if not time_maped:
                return
            self.timeValMap = gen_time_val_map(self)

        except Exception as e:  # work on python 3.x
            print(e)

    def get_first(self) -> TradeInfo:
        return self.clac_min('time')

    def clac_max(self, f: str) -> TradeInfo:
        return max(self.trades, key=lambda x: getattr(x.get_data(), f))

    def clac_min(self, f: str) -> TradeInfo:
        return min(self.trades, key=lambda x: getattr(x.get_data(), f))

    def to_struct(self) -> dict:
        ans = dict()
        for k, v in self.__dict__.items():
            if k == 'trades':
                # ans[k] = [r.get_data().__dict__ for r in self.trades]
                continue
            if type(v) == datetime:
                ans[k] = to_time_utc_iso(v)
                continue

            ans[k] = v

        return ans
