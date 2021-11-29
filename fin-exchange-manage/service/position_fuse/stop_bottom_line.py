from typing import List

from sqlalchemy.orm import Session

from dto.order_dto import OrderDto
from dto.position_dto import PositionDto
from service.position_fuse import dtos
from service.position_fuse.stoper import Stoper
from utils import position_utils, formula_utils, direction_utils


class StopBottomLineStep:

    def __init__(self, profitRate: float, fallRate: float, clearRate: float = 1):
        self.profitRate: float = profitRate
        self.clearRate: float = clearRate
        self.fallRate: float = fallRate

    def is_conformable(self, pos: PositionDto, lastPrice: float) -> bool:
        profit_price = self.get_profit_price()
        return direction_utils.is_high_price(pos.positionSide, profit_price, lastPrice)

    def get_profit_price(self, pos: PositionDto) -> float:
        return direction_utils.plus_price_by_rate(pos.positionSide, pos.entryPrice, self.profitRate)


class StopBottomLineDto(dtos.StopDto):

    def __init__(self, symbol: str, positionSide: str, steps: List[StopBottomLineStep], tags: List[str] = list()):
        super().__init__(symbol=symbol, positionSide=positionSide, tags=tags)
        self.steps: List[StopBottomLineStep] = steps


class StopBottomLine(Stoper[StopBottomLineDto]):

    def __init__(self, exchange_name: str, session: Session):
        super(StopBottomLine, self).__init__(exchange_name=exchange_name, session=session, state=dtos.StopState.LOSS)

    def get_abc_clazz(self) -> object:
        return StopBottomLine

    def load_vars(self):
        super(StopBottomLine, self).load_vars()
        self.dto.steps = sorted(self.dto.steps, key=lambda s: s.profitRate,reverse = True)

    def is_up_to_date(self) -> bool:
        for step in self.dto.steps:

        quantity: float = position_utils.get_abs_amt(self.position) * self.dto.clearRate
        product = self.productDao.get_by_prd_name(self.dto.symbol)
        quantity = self.productDao.fix_precision_amt(product, quantity)
        if quantity != self.currentStopOrdersInfo.origQty:
            return False
        return not formula_utils.is_difference_over_range(self.stopPrice, self.currentStopOrdersInfo.avgPrice,
                                                          self.dto.restopRate)

    def clean_old_orders(self) -> List[OrderDto]:
        self.orderClientService.clean_orders(symbol=self.position.symbol, currentOds=self.currentStopOrdersInfo.orders)
        return self.currentStopOrdersInfo.orders

    def stop(self) -> dtos.StopResult:
        ans = dtos.StopResult(stopState=self.state)
        ans.orders = [self.post_order()]
        ans.active = True
        return ans

    def is_conformable(self) -> bool:
        if not super().is_conformable():
            return False
        for step in self.dto.steps:
            if step.is_conformable(self.position,self.lastPrice):
                return True
        return False

    def post_order(self) -> OrderDto:
        quantity: float = position_utils.get_abs_amt(self.position) * self.dto.clearRate
        price: float = self.stopPrice if direction_utils.is_low_price(self.position.positionSide, self.lastPrice,
                                                                      self.stopPrice) else direction_utils.fall_price(
            self.position.positionSide, self.lastPrice, 1.005)
        return self.orderClientService.post_stop_market(prd_name=self.dto.symbol, price=price,
                                                        quantity=quantity,
                                                        positionSide=self.dto.positionSide, tags=self.tags)
