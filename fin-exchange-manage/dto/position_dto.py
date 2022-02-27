class PositionDto:

    def __init__(self, entryPrice: float, isAutoAddMargin: bool, leverage: float, maxNotionalValue: float,
                 liquidationPrice: float, markPrice: float, positionAmt: float, symbol: str, unrealizedProfit: float,
                 marginType: str, isolatedMargin: float, positionSide: str, **kwargs):
        self.entryPrice: float = entryPrice
        self.isAutoAddMargin: bool = isAutoAddMargin  # unused
        self.leverage: float = leverage
        self.maxNotionalValue: float = maxNotionalValue
        self.liquidationPrice: float = liquidationPrice
        self.markPrice: float = markPrice
        self.positionAmt: float = positionAmt
        self.symbol: str = symbol
        self.unrealizedProfit: float = unrealizedProfit
        self.marginType: str = marginType  # unused
        self.isolatedMargin: float = isolatedMargin  # unused
        self.positionSide: str = positionSide


class PositionFilter:

    def __init__(self, symbol: str = None, positionSide: str = None, **kwargs):
        self.symbol = symbol
        self.positionSide = positionSide
