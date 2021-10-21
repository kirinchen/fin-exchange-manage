import abc
from abc import ABCMeta, ABC
from typing import TypeVar, Generic, List

import exchange
import rest.account.info.get
from dto.account_dto import AccountDto
from dto.order_dto import OrderDto
from dto.position_dto import PositionDto
from dto.post_order_dto import BasePostOrderDto, PostLimitOrderDto
from rest import account
from service.base_exchange_abc import BaseExchangeAbc
from service.position_client_service import PositionClientService
from service.trade_client_service import TradeClientService
from utils import direction_utils, comm_utils


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

    def __init__(self, exchange_name: str):
        super(BaseOrderBuilder, self).__init__(exchange_name)
        self.dto: T = None
        self.tradeClientService: TradeClientService = None
        self.positionClientService: PositionClientService = None

    def init(self, dto: T):
        self.dto = dto
        self.tradeClientService: TradeClientService = exchange.gen_impl_obj(self.exchange, TradeClientService)
        self.positionClientService: PositionClientService = exchange.gen_impl_obj(self.exchange, PositionClientService)

    def get_current_position(self) -> PositionDto:
        return self.positionClientService.find_one(symbol=self.dto.symbol, positionSide=self.dto.positionSide)

    def post(self) -> List[OrderDto]:
        ans: List[OrderDto] = list()
        for pq in self.gen_price_qty_list():
            ans.append(self.post_one(pq))
        return ans

    @abc.abstractmethod
    def load_data(self) -> LoadDataCheck:
        raise NotImplementedError('load_data')

    @abc.abstractmethod
    def get_order_side(self) -> str:
        raise NotImplementedError('get_order_side')

    @abc.abstractmethod
    def gen_price_qty_list(self) -> List[PriceQty]:
        raise NotImplementedError('gen_price_qty_list')

    @abc.abstractmethod
    def post_one(self, pq: PriceQty) -> OrderDto:
        raise NotImplementedError('post_one')


class LimitOrderBuilder(BaseOrderBuilder[PostLimitOrderDto], ABC):

    def __init__(self, exchange: str):
        super(LimitOrderBuilder, self).__init__(exchange)
        self.account: AccountDto = None
        self.position: PositionDto = None
        self.amount: float = None
        self.lastPrice: float = None

    def get_abc_clazz(self) -> object:
        return LimitOrderBuilder

    def load_data(self) -> LoadDataCheck:
        self.position = self.get_current_position()
        self.account = account.info.get.invoke(self.exchange)
        self.amount = self.account.maxWithdrawAmount * self.dto.withdrawAmountRate
        self.lastPrice = self.tradeClientService.get_last_fall_price(symbol=self.dto.symbol,
                                                                     positionSide=self.dto.positionSide,
                                                                     buffRate=self.dto.priceBuffRate)
        minUsdAmt: float = self.dto.get_symbol().get_min_usd_amount(self.lastPrice)
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
            p = self.lastPrice * (1 + self.dto.gapRate)
            pre_amt: float = base_amt * pow(self.dto.proportionalRate, i)
            qty: float = self._calc_quantity(quote=p, amount=pre_amt)
            priceQtyList.append(PriceQty(
                price=p,
                quantity=qty
            ))
        return priceQtyList
