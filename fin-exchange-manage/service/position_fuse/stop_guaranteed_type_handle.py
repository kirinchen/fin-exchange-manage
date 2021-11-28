import abc
from abc import ABCMeta
from enum import Enum
from typing import List

from dto.order_dto import OrderDto
from dto.position_dto import PositionDto
from infra import constant
from model import Product
from service.order_client_service import OrderClientService
from service.product_dao import ProductDao
from utils import order_utils, formula_utils, direction_utils
from utils.order_utils import OrdersInfo, OrderFilter

GUARANTEED_ORDER_TAG = 'gntop'


class TypeOrderHandle(metaclass=ABCMeta):

    def __init__(self, position: PositionDto, orderClient: OrderClientService):
        self.position: PositionDto = position
        self.orderClient: OrderClientService = orderClient
        self.productDao: ProductDao = orderClient.get_ex_obj(ProductDao)
        self.product: Product = self.productDao.get_by_prd_name(position.symbol)
        self.currentOrders: List[OrderDto] = list()

    def init_vars(self):
        pass

    @abc.abstractmethod
    def is_up_to_date(self) -> bool:
        return NotImplemented

    def clean_old_orders(self) -> List[OrderDto]:
        self.orderClient.clean_orders(symbol=self.position.symbol, currentOds=self.currentStopOrderInfo.orders)
        return self.currentStopOrderInfo.orders

    @abc.abstractmethod
    def post_order(self, tags: List[str]) -> List[OrderDto]:
        return NotImplemented


class GuaranteedState(Enum):
    IDLE = 'IDLE'  # no any Filled or new stop order
    DONE = 'DONE'  # just amt / price is ok and no new order
    CORRECT = 'CORRECT'  # just amt / price + no new order
    CHAOS_CURRENT = 'CHAOS_CURRENT'


class GuaranteedOrderHandle(TypeOrderHandle):

    def __init__(self, position: PositionDto, orderClient: OrderClientService, guaranteed_price: float,
                 guaranteed_amt: float):
        super(GuaranteedOrderHandle, self).__init__(position=position, orderClient=orderClient)
        self.guaranteed_price: float = guaranteed_price
        self.guaranteed_amt: float = guaranteed_amt
        self.currentStopOrderInfo: OrdersInfo = None

    def init_vars(self):
        self.currentStopOrderInfo: OrdersInfo = order_utils.filter_order(self.currentOrders, OrderFilter(
            tags=[GUARANTEED_ORDER_TAG]
        ))

    def post_order(self, tags: List[str]) -> List[OrderDto]:
        n_tag = list(tags)
        n_tag.append(GUARANTEED_ORDER_TAG)
        return [self.orderClient.post_stop_market(prd_name=self.position.symbol
                                                  , price=self.guaranteed_price
                                                  , quantity=self.guaranteed_amt
                                                  , positionSide=self.position.positionSide
                                                  , tags=n_tag)]

    def get_state(self) -> GuaranteedState:
        if self.currentStopOrderInfo.origQty <= 0:
            return GuaranteedState.IDLE

        if formula_utils.is_difference_over_range(
                self.productDao.fix_precision_amt(self.product, self.currentStopOrderInfo.origQty),
                self.productDao.fix_precision_amt(self.product, self.guaranteed_amt),
                constant.LIMIT_0_RATE):
            return GuaranteedState.CHAOS_CURRENT
        currentAvgPrice: float = self.currentStopOrderInfo.avgPrice
        return GuaranteedState.CHAOS_CURRENT if formula_utils.is_difference_over_range(
            self.productDao.fix_precision_price(self.product, currentAvgPrice),
            self.productDao.fix_precision_price(self.product, self.guaranteed_price),
            constant.LIMIT_0_RATE) else GuaranteedState.DONE

    def is_up_to_date(self) -> bool:
        """
        True : 有 Filled 然後是 GUARANTEED_ORDER_TAG 的Order
        False : 有
        False : 沒有 或是 stop order 不正確
        """
        state = self.get_state()
        return state == GuaranteedState.DONE


class BaseState(Enum):
    IDLE = 'IDLE'  # no any Filled or new stop order
    DONE = 'DONE'  # just amt / price is ok and no new order
    CHAOS = 'CHAOS'  # 現在的 order 就是不對


class BaseOrderHandle(TypeOrderHandle):

    def __init__(self, position: PositionDto, orderClient: OrderClientService, stopPrice: float, stopAmt: float):
        super(BaseOrderHandle, self).__init__(position=position, orderClient=orderClient)
        self.currentStopOrderInfo: OrdersInfo = None
        self.stopPrice: float = stopPrice
        self.stopAmt: float = stopAmt

    def init_vars(self):
        self.currentStopOrderInfo: OrdersInfo = OrdersInfo(orders=self.currentOrders, group=None)
        self.currentStopOrderInfo.subtotal()

    def get_state(self) -> BaseState:
        if self.currentStopOrderInfo.origQty <= 0:
            return BaseState.IDLE
        if formula_utils.is_difference_over_range(
                self.productDao.fix_precision_price(self.product, self.stopPrice),
                self.productDao.fix_precision_price(self.product, self.currentStopOrderInfo.avgPrice),
                constant.LIMIT_0_RATE):
            return BaseState.CHAOS
        return BaseState.CHAOS if formula_utils.is_difference_over_range(
            self.productDao.fix_precision_amt(self.product, self.currentStopOrderInfo.origQty),
            self.productDao.fix_precision_amt(self.product, self.stopAmt),
            constant.LIMIT_0_RATE) else BaseState.DONE

    def is_up_to_date(self) -> bool:
        state = self.get_state()
        return state == BaseState.DONE

    def post_order(self, tags: List[str]) -> List[OrderDto]:

        return [self.orderClient.post_stop_market(prd_name=self.position.symbol
                                                  , price=self.stopPrice
                                                  , quantity=self.stopAmt
                                                  , positionSide=self.position.positionSide
                                                  , tags=tags)]


class HandleBundle:

    def __init__(self, guaranteed: GuaranteedOrderHandle, base: BaseOrderHandle):
        self.guaranteed: GuaranteedOrderHandle = guaranteed
        self.base: BaseOrderHandle = base


def gen_type_order_handle(position: PositionDto,
                          currentStopOrdersInfo: OrdersInfo,
                          guaranteed_price: float,
                          guaranteed_amt: float,
                          stopPrice: float,
                          stopAmt: float,
                          orderClientService: OrderClientService,
                          **kwargs) -> HandleBundle:
    base = BaseOrderHandle(position=position, stopPrice=stopPrice, stopAmt=stopAmt, orderClient=orderClientService)
    guaranteed = GuaranteedOrderHandle(position=position, guaranteed_price=guaranteed_price,
                                       guaranteed_amt=guaranteed_amt, orderClient=orderClientService)
    for od in currentStopOrdersInfo.orders:
        if direction_utils.is_low_price(position.positionSide, position.entryPrice, od.stopPrice):
            base.currentOrders.append(od)
        else:
            guaranteed.currentOrders.append(od)

    guaranteed.init_vars()
    base.init_vars()

    return HandleBundle(
        guaranteed=guaranteed,
        base=base
    )
