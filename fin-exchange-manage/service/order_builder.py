import abc
from abc import ABC
from typing import TypeVar, Generic, List

from sqlalchemy.orm import Session

import exchange
import rest.account.info.get
from dto.account_dto import AccountDto
from dto.order_dto import OrderDto
from dto.position_dto import PositionDto
from dto.post_order_dto import BasePostOrderDto, PostLimitOrderDto, PostTakeStopProfitDto
from infra.enums import OrderStrategy
from model import Product
from model.init_data import init_item
from rest import account
from rest.proxy_controller import PayloadReqKey
from service.base_exchange_abc import BaseExchangeAbc
from service.order_client_service import OrderClientService
from service.position_client_service import PositionClientService
from service.product_dao import ProductDao
from service.trade_client_service import TradeClientService
from utils import direction_utils, comm_utils, position_utils


class PriceQty:

    def __init__(self, price: float, quantity: float):
        self.price: float = price
        self.quantity: float = quantity


class LoadDataCheck:

    def __init__(self, success: bool, failsMsg: str = None):
        self.success: bool = success
        self.failsMsg: str = failsMsg


T = TypeVar('T', bound=BasePostOrderDto)


class BaseOrderBuilder(Generic[T], BaseExchangeAbc, ABC):

    def __init__(self, exchange_name: str, session: Session = None):
        super(BaseOrderBuilder, self).__init__(exchange_name, session)
        self.dto: T = None
        self.tradeClientService: TradeClientService = None
        self.positionClientService: PositionClientService = None
        self.orderClientService: OrderClientService = None
        self.productDao: ProductDao = None
        self.product: Product = None
        self.lastPrice: float = None

    def init(self, dto: T) -> object:
        self.dto = dto
        self.tradeClientService: TradeClientService = exchange.gen_impl_obj(self.exchange_name, TradeClientService,
                                                                            self.session)
        self.positionClientService: PositionClientService = exchange.gen_impl_obj(self.exchange_name,
                                                                                  PositionClientService,
                                                                                  self.session)
        self.orderClientService: OrderClientService = exchange.gen_impl_obj(self.exchange_name, OrderClientService,
                                                                            self.session)
        self.productDao: ProductDao = exchange.gen_impl_obj(self.exchange_name, ProductDao, self.session)
        self.product = self.productDao.get_by_prd_name(self.dto.symbol)
        return self

    def get_current_position(self) -> PositionDto:
        return self.positionClientService.find_one(symbol=self.dto.symbol, positionSide=self.dto.positionSide)

    def post(self) -> List[OrderDto]:
        ans: List[OrderDto] = list()
        for pq in self.gen_price_qty_list():
            ans.append(self.post_one(pq))
        return ans

    def calc_proportional_amt(self, per_qty: float, i: int) -> float:
        num = self.dto.size - i if self.dto.proportionalReverse else i
        return per_qty * pow(self.dto.proportionalRate, num)

    def _valid_calc_price(self):
        if self.dto.gapRate < 0 and self.dto.targetPrice < 0:
            raise TypeError(f'gapRate={self.dto.gapRate} targetPrice={self.dto.targetPrice} tow <0')
        if self.dto.gapRate > 0 and self.dto.targetPrice > 0:
            raise TypeError(f'gapRate={self.dto.gapRate} targetPrice={self.dto.targetPrice} tow >0')

    def calc_rise_price(self, idx: int) -> float:
        self._valid_calc_price()
        if self.dto.gapRate > 0:
            return direction_utils.rise_price(positionSide=self.dto.positionSide, orgPrice=self.lastPrice,
                                              rate=1 + (self.dto.gapRate * idx))
        else:
            highPrice = direction_utils.get_high_price(positionSide=self.dto.positionSide, a=self.lastPrice,
                                                       b=self.dto.targetPrice)
            dp = (highPrice - self.lastPrice) / self.dto.size
            return self.lastPrice + (dp * (idx + self.dto.targetIdxShift))

    def calc_fall_price(self, idx: int) -> float:
        self._valid_calc_price()
        if self.dto.gapRate > 0:
            return direction_utils.fall_price(positionSide=self.dto.positionSide, orgPrice=self.lastPrice,
                                              rate=1 + (self.dto.gapRate * idx))
        else:
            lowPrice = direction_utils.get_low_price(positionSide=self.dto.positionSide, a=self.lastPrice,
                                                     b=self.dto.targetPrice)
            dp = (lowPrice - self.lastPrice) / self.dto.size
            return self.lastPrice + (dp * (idx + self.dto.targetIdxShift))

    @abc.abstractmethod
    def load_data(self) -> LoadDataCheck:
        raise NotImplementedError('load_data')

    @abc.abstractmethod
    def gen_price_qty_list(self) -> List[PriceQty]:
        raise NotImplementedError('gen_price_qty_list')

    @abc.abstractmethod
    def post_one(self, pq: PriceQty) -> OrderDto:
        raise NotImplementedError('post_one')


class LimitOrderBuilder(BaseOrderBuilder[PostLimitOrderDto], ABC):

    def __init__(self, exchange_name: str, session: Session):
        super(LimitOrderBuilder, self).__init__(exchange_name, session)
        self.account: AccountDto = None
        self.position: PositionDto = None
        self.amount: float = None

    def get_abc_clazz(self) -> object:
        return LimitOrderBuilder

    def load_data(self) -> LoadDataCheck:
        self.position = self.get_current_position()
        self.account = account.info.get.invoke(self.exchange_name)
        self.amount = self.account.maxWithdrawAmount * self.dto.withdrawAmountRate
        self.lastPrice = self.tradeClientService.get_last_fall_price(symbol=self.dto.symbol,
                                                                     positionSide=self.dto.positionSide,
                                                                     buffRate=self.dto.priceBuffRate)
        minUsdAmt: float = self.productDao.get_min_valuation_item_amount(product=self.product,
                                                                         price=self.lastPrice)
        leverage_amt: float = self.amount * self.position.leverage
        if minUsdAmt > leverage_amt:
            return LoadDataCheck(success=False, failsMsg=f'not have enough {minUsdAmt} > {leverage_amt}')
        return LoadDataCheck(success=True)

    def get_order_side(self) -> str:
        return direction_utils.get_limit_order_side(self.dto.positionSide)

    def _calc_quantity(self, quote: float, amount: float) -> float:
        max_ratio = self.position.maxNotionalValue / amount
        ratio = min(max_ratio, self.position.leverage)
        quantity = (amount * ratio) / quote
        return quantity

    def gen_price_qty_list(self) -> List[PriceQty]:

        base_amt: float = comm_utils.calc_proportional_first(sum=self.amount, rate=self.dto.proportionalRate,
                                                             n=self.dto.size)

        priceQtyList: List[PriceQty] = list()
        for i in range(int(self.dto.size)):
            p = self.calc_fall_price(i)
            pre_amt: float = self.calc_proportional_amt(base_amt, i)
            qty: float = self._calc_quantity(quote=p, amount=pre_amt)
            priceQtyList.append(PriceQty(
                price=p,
                quantity=qty
            ))
        return priceQtyList

    def post_one(self, pq: PriceQty) -> OrderDto:
        return self.orderClientService.post_limit(prd_name=self.dto.symbol, price=pq.price, quantity=pq.quantity,
                                                  positionSide=self.dto.positionSide, tags=self.dto.tags)


class TakeProfitOrderBuilder(BaseOrderBuilder[PostTakeStopProfitDto], ABC):

    def __init__(self, exchange_name: str, session: Session = None):
        super().__init__(exchange_name, session)
        self.position_quantity: float = None
        self.position: PositionDto = None

    def load_data(self) -> LoadDataCheck:
        self.position = self.get_current_position()
        self.position_quantity: float = position_utils.get_abs_amt(self.position)
        self.lastPrice = self.get_last_price()
        if self.position_quantity <= 0:
            return LoadDataCheck(success=False, failsMsg='no has position amt')
        return LoadDataCheck(success=True)

    def get_last_price(self) -> float:
        return self.tradeClientService.get_last_rise_price(symbol=self.dto.symbol,
                                                           positionSide=self.dto.positionSide,
                                                           buffRate=self.dto.priceBuffRate)

    def get_abc_clazz(self) -> object:
        return TakeProfitOrderBuilder

    def gen_price_qty_list(self) -> List[PriceQty]:
        part_qty: float = self.position_quantity * self.dto.positionRate
        per_qty: float = comm_utils.calc_proportional_first(sum=part_qty, rate=self.dto.proportionalRate,
                                                            n=self.dto.size)
        priceQtyList: List[PriceQty] = list()
        for i in range(int(self.dto.size)):
            p = self.calc_price(i)
            q = self.calc_proportional_amt(per_qty, i)
            priceQtyList.append(PriceQty(
                price=p,
                quantity=q
            ))
        return priceQtyList

    def calc_price(self, idx: int) -> float:
        return self.calc_rise_price(idx)

    def post_one(self, pq: PriceQty) -> OrderDto:
        return self.orderClientService.post_take_profit(prd_name=self.dto.symbol, price=pq.price, quantity=pq.quantity,
                                                        positionSide=self.dto.positionSide, tags=self.dto.tags)


class StopMarketOrderBuilder(TakeProfitOrderBuilder, ABC):

    def get_abc_clazz(self) -> object:
        return StopMarketOrderBuilder

    def get_last_price(self) -> float:
        return self.tradeClientService.get_last_fall_price(symbol=self.dto.symbol,
                                                           positionSide=self.dto.positionSide,
                                                           buffRate=self.dto.priceBuffRate)

    def calc_price(self, idx: int) -> float:
        return self.calc_fall_price(idx)

    def post_one(self, pq: PriceQty) -> OrderDto:
        return self.orderClientService.post_stop_market(prd_name=self.dto.symbol, price=pq.price, quantity=pq.quantity,
                                                        positionSide=self.dto.positionSide, tags=self.dto.tags)


def gen_order_builder(session: Session, payload: dict) -> BaseOrderBuilder:
    strategy: str = payload.get('strategy')
    strategy: OrderStrategy = comm_utils.value_of_enum(OrderStrategy, strategy)
    if strategy == OrderStrategy.TAKE_PROFIT:
        return exchange.gen_impl_obj(exchange_name=PayloadReqKey.exchange.get_val(payload),
                                     clazz=TakeProfitOrderBuilder, session=session).init(
            PostTakeStopProfitDto(**payload))
    if strategy == OrderStrategy.STOP_MARKET:
        return exchange.gen_impl_obj(exchange_name=PayloadReqKey.exchange.get_val(payload),
                                     clazz=StopMarketOrderBuilder, session=session).init(
            PostTakeStopProfitDto(**payload))
    if strategy == OrderStrategy.LIMIT:
        return exchange.gen_impl_obj(exchange_name=PayloadReqKey.exchange.get_val(payload),
                                     clazz=LimitOrderBuilder, session=session).init(
            PostLimitOrderDto(**payload))
    raise NotImplementedError(f'not Implemented {strategy} ')
