from typing import List

from dto.position_dto import PositionDto, PositionFilter


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


def get_abs_amt(p: PositionDto) -> float:
    return abs(p.positionAmt)
