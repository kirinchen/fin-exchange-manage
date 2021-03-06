from datetime import datetime

from utils import reflection_util


class CandlestickDto:

    def __init__(self, **kwargs):
        self.openAt: datetime = None
        self.open = 0.0
        self.high = 0.0
        self.low = 0.0
        self.close = 0.0
        self.volume = 0.0
        self.closeAt: datetime = None
        self.quoteAssetVolume = 0.0
        self.numTrades = 0
        self.takerBuyBaseAssetVolume = 0.0
        self.takerBuyQuoteAssetVolume = 0.0
        self.ignore = 0.0
        self.highAt: datetime = None
        self.lowAt: datetime = None
        reflection_util.merge(kwargs, self)
