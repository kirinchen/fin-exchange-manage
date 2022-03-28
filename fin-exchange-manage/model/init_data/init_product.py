from typing import List

from model import Product
from model.init_data import DataInit, init_exchange, init_item


class InitProduct(DataInit[Product]):

    def __init__(self):
        item = init_item.get_instance()
        _exchange = init_exchange.get_instance()
        # --- binance start ---
        self.btc_binance = Product(exchange=_exchange.binance.name,
                                   item=item.btc.name,
                                   prd_name=item.btc.symbol,
                                   valuation_item=item.usdt.name,
                                   )
        self.bch_binance = Product(exchange=_exchange.binance.name,
                                   item=item.bch.name,
                                   prd_name=item.bch.symbol,
                                   valuation_item=item.usdt.name,
                                   )
        self.eth_binance = Product(exchange=_exchange.binance.name,
                                   item=item.eth.name,
                                   prd_name=item.eth.symbol,
                                   valuation_item=item.usdt.name,
                                   )
        self.etc_binance = Product(exchange=_exchange.binance.name,
                                   item=item.etc.name,
                                   prd_name=item.etc.symbol,
                                   valuation_item=item.usdt.name,
                                   )
        self.ltc_binance = Product(exchange=_exchange.binance.name,
                                   item=item.ltc.name,
                                   prd_name=item.ltc.symbol,
                                   valuation_item=item.usdt.name,
                                   )
        self.xrp_binance = Product(exchange=_exchange.binance.name,
                                   item=item.xrp.name,
                                   prd_name=item.xrp.symbol,
                                   valuation_item=item.usdt.name,
                                   )
        self.eos_binance = Product(exchange=_exchange.binance.name,
                                   item=item.eos.name,
                                   prd_name=item.eos.symbol,
                                   valuation_item=item.usdt.name,
                                   )
        self.bnb_binance = Product(exchange=_exchange.binance.name,
                                   item=item.bnb.name,
                                   prd_name=item.bnb.symbol,
                                   valuation_item=item.usdt.name,
                                   )
        self.dot_binance = Product(exchange=_exchange.binance.name,
                                   item=item.dot.name,
                                   prd_name=item.dot.symbol,
                                   valuation_item=item.usdt.name,
                                   )
        self.ada_binance = Product(exchange=_exchange.binance.name,
                                   item=item.ada.name,
                                   prd_name=item.ada.symbol,
                                   valuation_item=item.usdt.name,
                                   )
        # --- binance end ---
        # --- maicoin_max start ---
        self.btc_maicoin_max = Product(exchange=_exchange.maicoin_max.name,
                                       item=item.btc.name,
                                       prd_name=f'{item.btc.symbol}{item.twd.symbol}',
                                       valuation_item=item.twd.name,
                                       )
        self.bch_maicoin_max = Product(exchange=_exchange.maicoin_max.name,
                                       item=item.bch.name,
                                       prd_name=f'{item.bch.symbol}{item.twd.symbol}',
                                       valuation_item=item.twd.name,
                                       )
        self.eth_maicoin_max = Product(exchange=_exchange.maicoin_max.name,
                                       item=item.eth.name,
                                       prd_name=f'{item.eth.symbol}{item.twd.symbol}',
                                       valuation_item=item.twd.name,
                                       )
        self.ltc_maicoin_max = Product(exchange=_exchange.maicoin_max.name,
                                       item=item.ltc.name,
                                       prd_name=f'{item.ltc.symbol}{item.twd.symbol}',
                                       valuation_item=item.twd.name,
                                       )
        self.xrp_maicoin_max = Product(exchange=_exchange.maicoin_max.name,
                                       item=item.xrp.name,
                                       prd_name=f'{item.xrp.symbol}{item.twd.symbol}',
                                       valuation_item=item.twd.name,
                                       )
        # --- maicoin_max end ---

    def get_clazz(self) -> Product:
        return Product

    def gen_data(self) -> List[Product]:
        ans: List[Product] = list()
        for k, v in self.__dict__.items():
            ans.append(v)
        return ans


def get_instance() -> InitProduct:
    return InitProduct()
