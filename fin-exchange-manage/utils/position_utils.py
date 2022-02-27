from typing import List

from dto.order_dto import OrderDto
from dto.position_dto import PositionDto, PositionFilter
from dto.wallet_dto import WalletDto
from infra.enums import OrderStatus, OrderSide
from utils import order_utils
from utils.order_utils import OrderFilter


def find_position_one(ps: List[PositionDto], symbol: str, positionSide: str) -> PositionDto:
    pf = PositionFilter(symbol=symbol, positionSide=positionSide)
    return filter_position(ps, pf)[0]


def filter_position(ps: List[PositionDto], ft: PositionFilter) -> List[PositionDto]:
    ans: List[PositionDto] = list()
    for p in ps:

        if ft.symbol and ft.symbol != p.symbol:
            continue
        if ft.positionSide and ft.positionSide != p.positionSide:
            continue
        ans.append(p)
    return ans


def get_by_orders(amt: float, prd_name: str, orders: List[OrderDto]) -> PositionDto:
    sumPrice = 0.0
    _sumAmt = 0.0
    for od in orders:
        if od.side == OrderSide.BUY:
            sumPrice += od.price * od.executedQty
            _sumAmt += od.executedQty
        if od.side == OrderSide.SELL:
            sumPrice -= od.price * od.executedQty
            _sumAmt -= od.executedQty
        if _sumAmt == amt:
            break
    if _sumAmt!=amt:



def get_abs_amt(p: PositionDto) -> float:
    return abs(p.positionAmt)
