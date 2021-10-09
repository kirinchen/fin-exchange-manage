from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Any

from rest.poxy_controller import PayloadReqKey

T = TypeVar("T")


class Function(ABC, Generic[T]):

    @abstractmethod
    def func(self, payload: dict) -> T:
        raise NotImplementedError()


def proxy_exchange(payload: dict, clazz: T) -> Function[T]:
    ex: str = PayloadReqKey.exchange.get_val(payload)
