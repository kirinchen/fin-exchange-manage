from datetime import datetime

from utils import reflection_util


class CandlestickDto:

    def __init__(self, **kwargs):
        self.openTime: datetime = None
        self.open = 0.0
        self.high = 0.0
        self.low = 0.0
        self.close = 0.0
        self.volume = 0.0
        self.closeTime: datetime = None
        self.quoteAssetVolume = 0.0
        self.numTrades = 0
        self.takerBuyBaseAssetVolume = 0.0
        self.takerBuyQuoteAssetVolume = 0.0
        self.ignore = 0.0
        reflection_util.merge(kwargs, self)
