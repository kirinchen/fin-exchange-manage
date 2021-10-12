from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Any

import exchange
from rest.proxy_controller import PayloadReqKey

T = TypeVar("T")


class APIFunction(ABC, Generic[T]):

    @abstractmethod
    def func(self, payload: dict) -> T:
        raise NotImplementedError()


def proxy_exchange(payload: dict) -> APIFunction[T]:
    ex: str = PayloadReqKey.exchange.get_val(payload)
    name: str = PayloadReqKey.name.get_val(payload)
    return exchange.load_function(exchange=ex, name=name)
