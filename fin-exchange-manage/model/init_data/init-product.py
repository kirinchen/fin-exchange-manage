from typing import List

from model import Product
from model.init_data import DataInit, T


class InitProduct(DataInit[Product]):

    def get_clazz(self) -> T:
        return Product

    def gen_data(self) -> List[Product]:
        ans: List[Product] = list()
        ans.append(Product(
            name='Bitcoin',
            symbol='BTC'
        ))
        ans.append(Product(
            name='Bitcoin Cash',
            symbol='BCH'
        ))
        return ans


def get_instance() -> DataInit:
    return InitProduct()
