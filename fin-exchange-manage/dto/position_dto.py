from utils import reflection_util


class PositionDto:

    def __init__(self,  **kwargs):
        self.entryPrice: float = None
        self.isAutoAddMargin: bool = None  # unused
        self.leverage: float = None
        self.maxNotionalValue: float = None
        self.liquidationPrice: float = None
        self.markPrice: float = None
        self.positionAmt: float = None
        self.symbol: str = None
        self.unrealizedProfit: float = None
        self.marginType: str = None  # unused
        self.isolatedMargin: float = None  # unused
        self.positionSide: str = None
        reflection_util.merge(kwargs, self)


class PositionFilter:

    def __init__(self, symbol: str = None, positionSide: str = None, **kwargs):
        self.symbol = symbol
        self.positionSide = positionSide
