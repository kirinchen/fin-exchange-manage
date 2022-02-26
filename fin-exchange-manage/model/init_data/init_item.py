from typing import List

from model import Item
from model.init_data import DataInit, T


class InitItem(DataInit[Item]):

    def __init__(self):
        self.usdt = Item(
            name='Tether',
            symbol='USDT'
        )
        self.twd = Item(
            name='TaiwanDollar',
            symbol='TWD'
        )
        self.btc = Item(
            name='Bitcoin',
            symbol='BTC'
        )
        self.bch = Item(
            name='Bitcoin Cash',
            symbol='BCH'
        )
        self.eth = Item(
            name='ethereum',
            symbol='ETH'
        )
        self.etc = Item(
            name='Ethereum Classic',
            symbol='ETC'
        )
        self.ltc = Item(
            name='Litecoin',
            symbol='LTC'
        )
        self.xrp = Item(
            name='XRP',
            symbol='XRP'
        )
        self.eos = Item(
            name='EOS',
            symbol='EOS'
        )
        self.bnb = Item(
            name='Binance Coin',
            symbol='BNB'
        )
        self.dot = Item(
            name='Polkadot',
            symbol='DOT'
        )
        self.ada = Item(
            name='Cardano',
            symbol='ADA'
        )

    def get_clazz(self) -> T:
        return Item

    def gen_data(self) -> List[Item]:
        ans: List[Item] = list()
        for k, v in self.__dict__.items():
            ans.append(v)
        return ans


def get_instance() -> InitItem:
    return InitItem()
