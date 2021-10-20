from typing import List

from model import ExchangeProduct
from model.init_data import DataInit, init_exchange, init_item


class InitExchangeProduct(DataInit[ExchangeProduct]):

    def __init__(self):
        item = init_item.get_instance()
        _exchange = init_exchange.get_instance()
        self.btc_binance = ExchangeProduct(exchange=_exchange.binance.name,
                                           item=item.btc.name,
                                           valuation_item=item.usdt.name,
                                           precision_price=
                                           )

    def get_clazz(self) -> ExchangeProduct:
        return ExchangeProduct

    def gen_data(self) -> List[ExchangeProduct]:
        ans: List[ExchangeProduct] = list()
        for k, v in self.__dict__.items():
            ans.append(v)
        return ans


def get_instance() -> InitExchangeProduct:
    return InitExchangeProduct()
