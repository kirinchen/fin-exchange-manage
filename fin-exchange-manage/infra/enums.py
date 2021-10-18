from enum import Enum


class OrderStrategy(Enum):
    TAKE_PROFIT = 'TAKE_PROFIT'
    LIMIT = 'LIMIT'


class PositionSide(Enum):
    BOTH = "BOTH"
    LONG = "LONG"
    SHORT = "SHORT"