from typing import List

from sqlalchemy.orm import Session

from dto.order_dto import OrderDto
from service.position_fuse import stop_guaranteed_type_handle
from service.position_fuse.mediation import StopDto, Stoper, StopState, StopResult
from service.position_fuse.stop_guaranteed_type_handle import HandleBundle
from utils import position_utils, direction_utils, formula_utils
from utils.formula_utils import GuaranteedBundle


class StopOrder:

    def __init__(self):
        self.base: List[OrderDto] = list()
        self.guaranteed: List[OrderDto] = list()


class StopGuaranteedDto(StopDto):
    def __init__(self, symbol: str, positionSide: str, closeRate: float, thresholdRate: float,
                 tags: List[str] = list()):
        super().__init__(symbol=symbol, positionSide=positionSide, tags=tags)
        self.closeRate: float = closeRate
        self.thresholdRate: float = thresholdRate


class StopGuaranteed(Stoper[StopGuaranteedDto]):

    def __init__(self, exchange_name: str, session: Session):
        super().__init__(exchange_name=exchange_name, session=session, state=StopState.GUARANTEED)
        self.stopPrice: float = None
        self.stopAmt: float = None
        self.guaranteed_price: float = None
        self.guaranteed_amt: float = None
        self.orderHandleBundle: HandleBundle = None

    def get_abc_clazz(self) -> object:
        return StopGuaranteed

    def load_vars(self):
        super().load_vars()
        self.stopPrice: float = self._calc_stop_price()
        self.guaranteed_price: float = formula_utils.calc_guaranteed_price(self.position.positionSide,
                                                                                 self._gen_guaranteed_bundle())
        self.guaranteed_amt: float = position_utils.get_abs_amt(self.position) * self.dto.closeRate
        self.stopAmt: float = position_utils.get_abs_amt(self.position) - self.guaranteed_amt
        self.orderHandleBundle = stop_guaranteed_type_handle.gen_type_order_handle(**self.__dict__)

    def is_conformable(self) -> bool:
        if not super().is_conformable():
            return False
        p: float = direction_utils.rise_price(self.position.positionSide, self.guaranteed_price, self.dto.thresholdRate)

        return position_stop_utils.is_valid_stop_price(self.position, self.lastPrice, p)

    def stop(self) -> StopResult:
        ods: List[OrderDto] = list()
        if not self.orderHandleBundle.guaranteed.is_up_to_date():
            ods.extend(self.orderHandleBundle.guaranteed.post_order(client=self.client, tags=self.tags))
        if not self.orderHandleBundle.base.is_up_to_date():
            ods.extend(self.orderHandleBundle.base.post_order(client=self.client, tags=self.tags))
        return StopResult(orders=ods, active=True, stopState=self.state)

    def is_up_to_date(self) -> bool:
        if not self.orderHandleBundle.guaranteed.is_up_to_date():
            return False
        if not self.orderHandleBundle.base.is_up_to_date():
            return False
        return True

    def clean_old_orders(self) -> List[OrderDto]:
        ans: List[OrderDto] = list()
        if not self.orderHandleBundle.guaranteed.is_up_to_date():
            ans.extend(self.orderHandleBundle.guaranteed.clean_old_orders(client=self.client))
        if not self.orderHandleBundle.base.is_up_to_date():
            ans.extend(self.orderHandleBundle.base.clean_old_orders(client=self.client))
        return ans

    def _gen_guaranteed_bundle(self) -> GuaranteedBundle:
        return GuaranteedBundle(
            closeRate=self.dto.closeRate,
            lever=self.position.leverage,
            amount=position_utils.get_abs_amt(self.position),
            price=self.position.entryPrice
        )

    def _calc_stop_price(self) -> float:
        amt: float = position_utils.get_abs_amt(self.position)
        guard_balance = (self.position.entryPrice * amt) / self.position.leverage
        return position_stop_utils.calc_guard_price(self.position, guard_balance)
