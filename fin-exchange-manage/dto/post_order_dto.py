from typing import List

from infra.enums import OrderStrategy
from utils import comm_utils


class BasePostOrderDto:

    def __init__(self, symbol: str, positionSide: str, strategy: str, priceBuffRate: float, gapRate: float = -1,
                 proportionalReverse: bool = False,
                 targetPrice: float = -1,
                 size: int = 1,
                 proportionalRate: float = 1,
                 targetIdxShift=0,
                 tags: List[str] = list(), attach: dict = None, attachName: str = None, **kwargs):
        self.strategy: str = strategy
        self.symbol: str = symbol
        self.positionSide: str = positionSide
        self.priceBuffRate: float = priceBuffRate
        self.targetIdxShift: int = targetIdxShift
        self.targetPrice: float = targetPrice if targetPrice is not None else -1
        self.gapRate: float = gapRate if gapRate is not None else -1
        self.proportionalRate: float = proportionalRate
        self.proportionalReverse: bool = proportionalReverse
        self.size: int = size
        self.tags: List[str] = list(tags)
        self.attach: dict = attach
        self.attachName: str = attachName

    def get_strategy(self) -> OrderStrategy:
        return comm_utils.value_of_enum(OrderStrategy, self.strategy)


class PostLimitOrderDto(BasePostOrderDto):

    def __init__(self, withdrawAmountRate: float, stopPrice: float = None, martingaleRate: float = 0,
                 closeLoseThreshold: float = -1, startPrice: float = -1,
                 **kwargs):
        super(PostLimitOrderDto, self).__init__(**kwargs)
        self.withdrawAmountRate: float = withdrawAmountRate
        self.startPrice: float = startPrice
        self.stopPrice: float = stopPrice
        self.martingaleRate: float = martingaleRate
        self.closeLoseThreshold: float = closeLoseThreshold


class PostTakeStopProfitDto(BasePostOrderDto):

    def __init__(self, positionRate: float, **kwargs):
        super(PostTakeStopProfitDto, self).__init__(**kwargs)
        self.positionRate: float = positionRate
