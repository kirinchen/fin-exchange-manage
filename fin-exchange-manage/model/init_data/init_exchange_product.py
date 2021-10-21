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
                                           precision_price=2,
                                           precision_amount=3
                                           )
        self.bch_binance = ExchangeProduct(exchange=_exchange.binance.name,
                                           item=item.bch.name,
                                           valuation_item=item.usdt.name,
                                           precision_price=2,
                                           precision_amount=3
                                           )
        self.eth_binance = ExchangeProduct(exchange=_exchange.binance.name,
                                           item=item.eth.name,
                                           valuation_item=item.usdt.name,
                                           precision_price=2,
                                           precision_amount=3
                                           )
        self.etc_binance = ExchangeProduct(exchange=_exchange.binance.name,
                                           item=item.etc.name,
                                           valuation_item=item.usdt.name,
                                           precision_price=3,
                                           precision_amount=2
                                           )
        self.ltc_binance = ExchangeProduct(exchange=_exchange.binance.name,
                                           item=item.ltc.name,
                                           valuation_item=item.usdt.name,
                                           precision_price=2,
                                           precision_amount=3
                                           )
        self.xrp_binance = ExchangeProduct(exchange=_exchange.binance.name,
                                           item=item.xrp.name,
                                           valuation_item=item.usdt.name,
                                           precision_price=4,
                                           precision_amount=1
                                           )
        self.eos_binance = ExchangeProduct(exchange=_exchange.binance.name,
                                           item=item.eos.name,
                                           valuation_item=item.usdt.name,
                                           precision_price=3,
                                           precision_amount=1
                                           )
        self.bnb_binance = ExchangeProduct(exchange=_exchange.binance.name,
                                           item=item.bnb.name,
                                           valuation_item=item.usdt.name,
                                           precision_price=2,
                                           precision_amount=2
                                           )
        self.dot_binance = ExchangeProduct(exchange=_exchange.binance.name,
                                           item=item.dot.name,
                                           valuation_item=item.usdt.name,
                                           precision_price=3,
                                           precision_amount=1
                                           )
        self.ada_binance = ExchangeProduct(exchange=_exchange.binance.name,
                                           item=item.ada.name,
                                           valuation_item=item.usdt.name,
                                           precision_price=4,
                                           precision_amount=0
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
