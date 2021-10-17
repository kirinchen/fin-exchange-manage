import abc
from abc import ABC


class BaseExchangeAbc(ABC):

    def __init__(self, exchange: str):
        self.exchange = exchange

    @abc.abstractmethod
    def get_abc_clazz(self) -> object:
        raise NotImplementedError()
