import config
from dto.position_dto import PositionDto
from infra.enums import PositionSide


def is_difference_over_range(source: float, target: float, rate: float):
    if source == 0 and target == 0:
        return False
    if source == 0 or target == 0:
        return True
    r: float = abs(1 - (target / source))
    return r > rate


def calc_guard_price(p: PositionDto, guard_balance: float, positionAmtRate: float = 1) -> float:
    positionAmt: float = p.positionAmt * positionAmtRate
    return -(guard_balance / positionAmt) + p.entryPrice


class GuaranteedBundle:

    def __init__(self, amount: float, price: float, lever: float, closeRate: float, exchange_name: str):
        self.exchange_name: str = exchange_name
        self.amount: float = amount
        self.price: float = price
        self.lever: float = lever
        self.closeRate: float = closeRate


def calc_guaranteed_price(positionSide: str, gb: GuaranteedBundle) -> float:
    return calc_guaranteed_long_price(gb) if positionSide == PositionSide.LONG else calc_guaranteed_short_price(gb)


def calc_guaranteed_long_price(i: GuaranteedBundle) -> float:
    maker_fee: float = config.env_float(i.exchange_name + '-maker-fee')
    taker_fee: float = config.env_float(i.exchange_name + '-taker-fee')
    numerator = i.price * (float(1) + (maker_fee * i.lever))
    denominator = i.lever * i.closeRate * (float(1) - taker_fee)
    return (numerator / denominator) + i.price


def calc_guaranteed_short_price(i: GuaranteedBundle) -> float:
    maker_fee: float = config.env_float(i.exchange_name + '-maker-fee')
    taker_fee: float = config.env_float(i.exchange_name + '-taker-fee')
    numerator = i.price * (float(1) + (maker_fee * i.lever) - (i.lever * i.closeRate) + (
            i.lever * i.closeRate * taker_fee))
    denominator = i.lever * i.closeRate * (float(1) - taker_fee)
    return - numerator / denominator
