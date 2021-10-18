import abc
from abc import ABCMeta, ABC
from typing import TypeVar, Generic, List

import rest.account.info.get
from dto.account_dto import AccountDto
from dto.order_dto import OrderDto
from dto.position_dto import PositionDto
from dto.post_order_dto import BasePostOrderDto, PostLimitOrderDto
from rest import account
from service.base_exchange_abc import BaseExchangeAbc


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

    def __init__(self, exchange: str):
        super(BaseOrderBuilder, self).__init__(exchange)
        self.dto: T = None

    def init(self, dto: T):
        self.dto = dto

    @abc.abstractmethod
    def get_current_position(self) -> PositionDto:
        raise NotImplementedError('get_current_position')

    def post(self) -> List[OrderDto]:
        ans: List[OrderDto] = list()
        for pq in self.gen_price_qty_list():
            ans.append(self.post_one(pq))
        return ans

    @abc.abstractmethod
    def load_data(self) -> LoadDataCheck:
        return NotImplemented

    @abc.abstractmethod
    def get_order_side(self) -> str:
        return NotImplemented

    @abc.abstractmethod
    def gen_price_qty_list(self) -> List[PriceQty]:
        return NotImplemented

    @abc.abstractmethod
    def post_one(self, pq: PriceQty) -> OrderDto:
        return NotImplemented


class LimitOrderBuilder(BaseOrderBuilder[PostLimitOrderDto]):

    def __init__(self, exchange: str):
        super(LimitOrderBuilder, self).__init__(exchange)
        self.account: AccountDto = None
        self.position: PositionDto = None
        self.amount: float = None
        self.lastPrice: float = None

    def load_data(self) -> LoadDataCheck:
        self.position = self.get_current_position()
        self.account = account.info.get.invoke(self.exchange)
        self.amount = self.account.maxWithdrawAmount * self.dto.withdrawAmountRate
        self.lastPrice = get_recent_trades_list.get_last_fall_price(client=self.client, symbol=self.dto.get_symbol(),
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

    def post_one(self, pq: PriceQty) -> Order:
        price_str = str(self.dto.get_symbol().fix_precision_price(pq.price))

        p_amt: float = self.dto.get_symbol().fix_precision_amt(pq.quantity)
        if p_amt == 0:
            return None
        quantity_str = str(p_amt)

        return self.client.post_order(price=price_str,
                                      side=self.get_order_side(),
                                      symbol=self.dto.get_symbol().gen_with_usdt(),
                                      timeInForce=TimeInForce.GTC,
                                      ordertype=OrderType.LIMIT,
                                      workingType=WorkingType.CONTRACT_PRICE,
                                      positionSide=self.dto.positionSide,
                                      # activationPrice=None,
                                      # closePosition=False,
                                      quantity=quantity_str,
                                      newClientOrderId=comm_utils.get_order_cid(tags=self.dto.tags)
                                      )
