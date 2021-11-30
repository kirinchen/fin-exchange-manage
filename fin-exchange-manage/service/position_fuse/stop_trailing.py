from typing import List

from sqlalchemy.orm import Session

from dto.order_dto import OrderDto
from dto.position_dto import PositionDto
from model import Product
from service.position_fuse import dtos
from service.position_fuse.stoper import Stoper
from service.product_dao import ProductDao
from utils import position_utils, formula_utils, direction_utils


class StopTrailingStep:

    def __init__(self, profitRate: float, fallRate: float, clearRate: float = 1):
        self.profitRate: float = profitRate
        self.clearRate: float = clearRate
        self.fallRate: float = fallRate

    def get_stop_price(self, pos: PositionDto, lastPrice: float) -> float:
        return direction_utils.plus_price_by_rate(pos.positionSide, lastPrice, -self.fallRate)

    def is_conformable(self, pos: PositionDto, lastPrice: float) -> bool:
        profit_price = self.get_profit_price(pos)
        return direction_utils.is_high_price(pos.positionSide, profit_price, lastPrice)

    def get_profit_price(self, pos: PositionDto) -> float:
        return direction_utils.plus_price_by_rate(pos.positionSide, pos.entryPrice, self.profitRate)

    def get_clear_amt(self, product: Product, pos: PositionDto) -> float:
        quantity: float = position_utils.get_abs_amt(pos) * self.clearRate
        return ProductDao.fix_precision_amt(product, quantity)


class StopTrailingDto(dtos.StopDto):

    def __init__(self, symbol: str, positionSide: str, steps: List[StopTrailingStep], restopRate: float,
                 tags: List[str] = list()):
        super().__init__(symbol=symbol, positionSide=positionSide, tags=tags)
        self.steps: List[StopTrailingStep] = [StopTrailingStep(**s) for s in steps]
        self.restopRate: float = restopRate


class StopTrailing(Stoper[StopTrailingDto]):

    def __init__(self, exchange_name: str, session: Session):
        super(StopTrailing, self).__init__(exchange_name=exchange_name, session=session, state=dtos.StopState.Trailing)

    def get_abc_clazz(self) -> object:
        return StopTrailing

    def load_vars(self):
        super(StopTrailing, self).load_vars()
        self.dto.steps = sorted(self.dto.steps, key=lambda s: s.profitRate, reverse=True)

    def is_up_to_date(self) -> bool:
        step = self.get_conformable_step()
        clear_amt = step.get_clear_amt(self.product, self.position)
        if clear_amt != self.currentStopOrdersInfo.origQty:
            return False
        cur_stop_price = self.currentStopOrdersInfo.avgPrice
        cur_stop_price = direction_utils.plus_price_by_rate(self.position.positionSide,cur_stop_price,self.dto.restopRate)
        want_stop_price = step.get_stop_price(self.position, self.lastPrice)
        return direction_utils.is_low_price(self.position.positionSide, cur_stop_price, want_stop_price)

    def clean_old_orders(self) -> List[OrderDto]:
        self.orderClientService.clean_orders(symbol=self.position.symbol, currentOds=self.currentStopOrdersInfo.orders)
        return self.currentStopOrdersInfo.orders

    def stop(self) -> dtos.StopResult:
        ans = dtos.StopResult(stopState=self.state)
        ans.orders = [self.post_order()]
        ans.active = True
        return ans

    def get_conformable_step(self) -> StopTrailingStep:
        for step in self.dto.steps:
            if step.is_conformable(self.position, self.lastPrice):
                return step
        return None

    def is_conformable(self) -> bool:
        if not super().is_conformable():
            return False
        return self.get_conformable_step() is not None

    def post_order(self) -> OrderDto:
        step = self.get_conformable_step()
        quantity: float = step.get_clear_amt(self.product, self.position)
        price: float = step.get_stop_price(self.position, self.lastPrice)
        return self.orderClientService.post_stop_market(prd_name=self.dto.symbol, price=price,
                                                        quantity=quantity,
                                                        positionSide=self.dto.positionSide, tags=self.tags)
