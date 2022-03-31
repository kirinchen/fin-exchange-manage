from typing import List

from model import Exchange
from model.init_data import DataInit


class InitExchange(DataInit[Exchange]):

    def __init__(self):
        self.binance = Exchange(name='binance', sides=['LONG', 'SHORT'])
        self.maicoin_max = Exchange(name='maicoin_max', sides=['LONG'])

    def get_clazz(self) -> Exchange:
        return Exchange

    def gen_data(self) -> List[Exchange]:
        ans: List[Exchange] = list()
        for k, v in self.__dict__.items():
            ans.append(v)
        return ans


def get_instance() -> InitExchange:
    return InitExchange()
