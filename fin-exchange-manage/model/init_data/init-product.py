from typing import List

from model import Item
from model.init_data import DataInit, T


class InitProduct(DataInit[Item]):

    def get_clazz(self) -> T:
        return Item

    def gen_data(self) -> List[Item]:
        ans: List[Item] = list()
        ans.append(Item(
            name='Bitcoin',
            symbol='BTC'
        ))
        ans.append(Item(
            name='Bitcoin Cash',
            symbol='BCH'
        ))
        return ans


def get_instance() -> DataInit:
    return InitProduct()
