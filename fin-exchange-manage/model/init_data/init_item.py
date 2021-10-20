from typing import List

from model import Item
from model.init_data import DataInit, T


class InitItem(DataInit[Item]):

    def __init__(self):
        self.usdt = Item(
            name='Tether',
            symbol='USDT'
        )
        self.btc = Item(
            name='Bitcoin',
            symbol='BTC'
        )
        self.bch = Item(
            name='Bitcoin Cash',
            symbol='BCH'
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
