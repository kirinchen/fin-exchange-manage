import abc
from abc import ABC
from typing import TypeVar

import exchange

EX = TypeVar('E')


class BaseExchangeAbc(ABC):

    def __init__(self, exchange_name: str, **kwargs):
        self.exchange_name = exchange_name
        self.payload = kwargs

    @abc.abstractmethod
    def get_abc_clazz(self) -> object:
        raise NotImplementedError()

    def get_ex_obj(self, ex: EX) -> EX:
        return exchange.gen_impl_obj(self.exchange_name, ex,
                                     **self.payload)


