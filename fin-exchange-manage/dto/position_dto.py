class PositionDto:

    def __init__(self, entryPrice: float, isAutoAddMargin: bool, leverage: float, maxNotionalValue: float,
                 liquidationPrice: float, markPrice: float, positionAmt: float, symbol: str, unrealizedProfit: float,
                 marginType: str, isolatedMargin: float, positionSide: str, **kwargs):
        self.entryPrice: float = entryPrice
        self.isAutoAddMargin: bool = isAutoAddMargin
        self.leverage: float = leverage
        self.maxNotionalValue: float = maxNotionalValue
        self.liquidationPrice: float = liquidationPrice
        self.markPrice: float = markPrice
        self.positionAmt: float = positionAmt
        self.symbol: str = symbol
        self.unrealizedProfit: float = unrealizedProfit
        self.marginType: str = marginType
        self.isolatedMargin: float = isolatedMargin
        self.positionSide: str = positionSide
