from datetime import datetime
from typing import List, Dict

import dateutil
import pytz

from dto.order_dto import OrderDto
from infra.enums import OrderType, OrderStatus
from utils import comm_utils, direction_utils


class OrderFilter:

    def __init__(self, symbol: str = None, side: str = None, orderType: str = None, notOrderType: str = None,
                 tags: List[str] = list(),
                 untags: List[str] = list(),
                 excludeTags: List[str] = list(),
                 status: str = None,
                 group: List[str] = list(),
                 updateStartAt: str = None,
                 updateEndAt: str = None,
                 limit: int = None,
                 positionSide: str = None, **kwargs):
        self.symbol = symbol
        self.side = side
        self.positionSide = positionSide
        self.tags = tags
        self.untags = untags
        self.excludeTags = excludeTags
        self.orderType = orderType
        self.notOrderType = notOrderType
        self.status = status
        self.updateStartTime: int = dateutil.parser.parse(updateStartAt).timestamp() * 1000 if updateStartAt else None
        self.updateEndTime: int = dateutil.parser.parse(updateEndAt).timestamp() * 1000 if updateEndAt else None
        self.group: List[str] = group
        self.limit: int = limit


class OrdersInfo:
    def __init__(self, orders: List[OrderDto], group: str):
        self.lastAt: datetime = None
        self.origQty = 0
        self.avgPrice = 0
        self.orders: List[OrderDto] = orders
        self.group: str = group
        self.groupMap: Dict[str, OrdersInfo] = dict()

    def subtotal(self):
        if len(self.orders) <= 0:
            return
        self.orders.sort(key=lambda s: s.updateTime, reverse=True)
        ups = self.orders[0].updateTime / 1000
        self.lastAt = datetime.fromtimestamp(ups, pytz.utc)
        sum_avg_price = 0
        for e in self.orders:
            e.updateAt = datetime.fromtimestamp(e.updateTime / 1000, pytz.utc).isoformat()
            self.origQty += e.origQty
            sum_avg_price += e.origQty * get_price(e)
        self.avgPrice = sum_avg_price / self.origQty
        if self.group:
            self.groupMap = self._group_by()

    def _group_by(self, ) -> Dict[str, object]:
        ans: Dict[str, OrdersInfo] = dict()
        for od in self.orders:
            groupv = getattr(od, self.group)
            g_sub_bundle = ans.get(groupv, OrdersInfo(group=None, orders=list()))
            g_sub_bundle.orders.append(od)
            ans[groupv] = g_sub_bundle
        for k, v in ans.items():
            v.subtotal()
        return ans

    def to_struct(self):

        ans = comm_utils.to_dict(self)
        ans['lastAt'] = self.lastAt.isoformat() if self.lastAt else None
        return ans


def get_price(od: OrderDto) -> float:
    if od.avgPrice > 0:
        return od.avgPrice
    if od.price > 0:
        return od.price
    if od.stopPrice > 0:
        return od.stopPrice
    raise NotImplementedError(f'the {od} not support any price')


def filter_order(oods: List[OrderDto], ft: OrderFilter) -> OrdersInfo:
    ans = OrdersInfo(group=ft.group[0] if ft.group else None, orders=list())
    for ods in oods:
        if ft.orderType and ods.type != ft.orderType:
            continue
        if ft.notOrderType and ods.type == ft.notOrderType:
            continue
        if ft.side and ods.side != ft.side:
            continue
        if ft.positionSide and ods.positionSide != ft.positionSide:
            continue
        if ft.symbol and ft.symbol != ods.symbol:
            continue
        if ft.status and ft.status != ods.status:
            continue
        if len(ft.tags) > 0 and not comm_utils.contains_tags(ods.clientOrderId, ft.tags):
            continue
        if len(ft.untags) > 0 and comm_utils.contains_tags(ods.clientOrderId, ft.untags):
            continue
        if len(ft.excludeTags) > 0 and comm_utils.contains_tags(ods.clientOrderId, ft.excludeTags):
            continue
        if ft.updateStartTime and ods.updateTime < ft.updateStartTime:
            continue
        if ft.updateEndTime and ods.updateTime > ft.updateEndTime:
            continue
        ans.orders.append(ods)
    ans.subtotal()
    return ans


def get_current_new_stop_orders(oods: List[OrderDto], symbol: str, positionSide: str) -> OrdersInfo:
    stop_order_side: str = direction_utils.get_stop_order_side(positionSide)
    of = OrderFilter(symbol=symbol.symbol,
                     orderType=OrderType.STOP_MARKET,
                     status=OrderStatus.NEW,
                     side=stop_order_side
                     )
    return filter_order(oods, of)
