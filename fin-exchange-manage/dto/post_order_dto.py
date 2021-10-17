from typing import List

from infra.enums import OrderStrategy
from utils import comm_utils


class BasePostOrderDto:

    def __init__(self, symbol: str, positionSide: str, strategy: str, priceBuffRate: float, gapRate: float,
                 size: int = 1,
                 proportionalRate: float = 1,
                 tags: List[str] = list(), **kwargs):
        self.strategy: str = strategy
        self.symbol: str = symbol
        self.positionSide: str = positionSide
        self.priceBuffRate: float = priceBuffRate
        self.gapRate: float = gapRate
        self.proportionalRate: float = proportionalRate
        self.size: int = size
        self.tags: List[str] = list(tags)

    def get_strategy(self) -> OrderStrategy:
        return comm_utils.value_of_enum(OrderStrategy, self.strategy)
