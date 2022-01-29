from enum import Enum


class OrderStrategy(Enum):
    TAKE_PROFIT = 'TAKE_PROFIT'
    LIMIT = 'LIMIT'
    STOP_MARKET = 'STOP_MARKET'
    FUSE_FIXED_STEP = 'FUSE_FIXED_STEP'


class PositionSide:
    BOTH = "BOTH"
    LONG = "LONG"
    SHORT = "SHORT"
    INVALID = None


class OrderSide:
    BUY = "BUY"
    SELL = "SELL"
    INVALID = None


class OrderType:
    LIMIT = "LIMIT"
    STOP_MARKET = "STOP_MARKET"
    TAKE_PROFIT = "TAKE_PROFIT"
    MARKET = 'MARKET'
    INVALID = None


class OrderStatus:
    NEW = "NEW"
    FILLED = "FILLED"
    PARTIALLY_FILLED = "PARTIALLY_FILLED"
    CANCELED = "CANCELED"
    PENDING_CANCEL = "PENDING_CANCEL"
    REJECTED = "REJECTED"
    EXPIRED = "EXPIRED"


class CandlestickInterval:
    MIN1 = "1m"
    MIN3 = "3m"
    MIN5 = "5m"
    MIN15 = "15m"
    MIN30 = "30m"
    HOUR1 = "1h"
    HOUR2 = "2h"
    HOUR4 = "4h"
    HOUR6 = "6h"
    HOUR8 = "8h"
    HOUR12 = "12h"
    DAY1 = "1d"
    DAY3 = "3d"
    WEEK1 = "1w"
    MON1 = "1m"
    INVALID = None
