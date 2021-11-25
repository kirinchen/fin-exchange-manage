from typing import List

from model import Product
from model.init_data import DataInit, init_exchange, init_item


class InitProduct(DataInit[Product]):

    def __init__(self):
        item = init_item.get_instance()
        _exchange = init_exchange.get_instance()
        self.btc_binance = Product(exchange=_exchange.binance.name,
                                   item=item.btc.name,
                                   prd_name=item.btc.name,
                                   valuation_item=item.usdt.name,
                                   precision_price=2,
                                   precision_amount=3
                                   )
        self.bch_binance = Product(exchange=_exchange.binance.name,
                                   item=item.bch.name,
                                   prd_name=item.bch.name,
                                   valuation_item=item.usdt.name,
                                   precision_price=2,
                                   precision_amount=3
                                   )
        self.eth_binance = Product(exchange=_exchange.binance.name,
                                   item=item.eth.name,
                                   prd_name=item.eth.name,
                                   valuation_item=item.usdt.name,
                                   precision_price=2,
                                   precision_amount=3
                                   )
        self.etc_binance = Product(exchange=_exchange.binance.name,
                                   item=item.etc.name,
                                   prd_name=item.etc.name,
                                   valuation_item=item.usdt.name,
                                   precision_price=3,
                                   precision_amount=2
                                   )
        self.ltc_binance = Product(exchange=_exchange.binance.name,
                                   item=item.ltc.name,
                                   prd_name=item.ltc.name,
                                   valuation_item=item.usdt.name,
                                   precision_price=2,
                                   precision_amount=3
                                   )
        self.xrp_binance = Product(exchange=_exchange.binance.name,
                                   item=item.xrp.name,
                                   prd_name=item.xrp.name,
                                   valuation_item=item.usdt.name,
                                   precision_price=4,
                                   precision_amount=1
                                   )
        self.eos_binance = Product(exchange=_exchange.binance.name,
                                   item=item.eos.name,
                                   prd_name=item.eos.name,
                                   valuation_item=item.usdt.name,
                                   precision_price=3,
                                   precision_amount=1
                                   )
        self.bnb_binance = Product(exchange=_exchange.binance.name,
                                   item=item.bnb.name,
                                   prd_name=item.bnb.name,
                                   valuation_item=item.usdt.name,
                                   precision_price=2,
                                   precision_amount=2
                                   )
        self.dot_binance = Product(exchange=_exchange.binance.name,
                                   item=item.dot.name,
                                   prd_name=item.dot.name,
                                   valuation_item=item.usdt.name,
                                   precision_price=3,
                                   precision_amount=1
                                   )
        self.ada_binance = Product(exchange=_exchange.binance.name,
                                   item=item.ada.name,
                                   prd_name=item.ada.name,
                                   valuation_item=item.usdt.name,
                                   precision_price=4,
                                   precision_amount=0
                                   )

    def get_clazz(self) -> Product:
        return Product

    def gen_data(self) -> List[Product]:
        ans: List[Product] = list()
        for k, v in self.__dict__.items():
            ans.append(v)
        return ans


def get_instance() -> InitProduct:
    return InitProduct()
