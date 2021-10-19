from typing import List

from dto.trade_dto import TradeSet, TradeDto


def gen_subtotal_result(ts: List[TradeDto], time_maped: bool = False) -> TradeSet:
    ans = TradeSet()
    for t in ts:
        ans.append(t)
    ans.subtotal(time_maped)
    return ans
