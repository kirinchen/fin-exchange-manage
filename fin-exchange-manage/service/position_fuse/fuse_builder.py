import abc
import math
from abc import ABC
from enum import Enum
from typing import TypeVar, Generic, List

from sqlalchemy.orm import Session

import exchange
from dto import order_dto
from dto.fuse_dto import BaseFuseDto, FixedStepFuseDto
from dto.order_dto import OrderDto
from dto.position_dto import PositionDto
from infra.enums import OrderStrategy
from model import OrderPack
from rest.proxy_controller import PayloadReqKey
from service.base_exchange_abc import BaseExchangeAbc
from service.order_client_service import OrderClientService
from service.order_pack_dao import OrderPackDao
from service.position_client_service import PositionClientService
from service.trade_client_service import TradeClientService
from utils import position_utils, comm_utils, direction_utils

FUSE_BASE_TAG = 'FS'


class PriceQty:

    def __init__(self, price: float, quantity: float):
        self.price: float = price
        self.quantity: float = quantity


class FuseResultType(Enum):
    NO_POSITION = 'NO_POSITION'
    NO_CRITERIA = 'NO_CRITERIA'
    UP_TO_DATE = 'UP_TO_DATE'
    EXECUTED = 'EXECUTED'


class FuseResult:

    def __init__(self, result_type: FuseResultType, closeOrders: List[OrderDto] = list(),
                 newOrders: List[OrderDto] = list()):
        self.resultType = result_type.value
        self.closeOrders: List[OrderDto] = closeOrders
        self.newOrders: List[OrderDto] = newOrders


class FusePrepareData:

    def __init__(self):
        self.position: PositionDto = None
        self.orderPack: OrderPack = None
        self.orders: List[OrderDto] = None
        self.currentPrice: float = None


T = TypeVar('T', bound=BaseFuseDto)


class BaseFuseBuilder(BaseExchangeAbc, Generic[T], ABC):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.prepareData: FusePrepareData = None
        self.dto: T = None
        self.positionClient: PositionClientService = None
        self.orderPackDao: OrderPackDao = None
        self.tradeClient: TradeClientService = None
        self.orderClient: OrderClientService = None

    def after_init(self):
        self.positionClient = self.get_ex_obj(PositionClientService)
        self.orderPackDao = self.get_ex_obj(OrderPackDao)
        self.tradeClient = self.get_ex_obj(TradeClientService)
        self.orderClient = self.get_ex_obj(OrderClientService)

    def init(self, dto: T, fuse_prepare_data=FusePrepareData()) -> object:
        self.dto = dto
        self.dto.tags.append(FUSE_BASE_TAG)
        self.prepareData: FusePrepareData = fuse_prepare_data
        self.prepareData.position = self.positionClient.find_one(self.dto.prd_name, self.dto.positionSide)
        odp, ods = self.orderPackDao.last({
            "exchange": self.exchange_name,
            "positionSide": self.dto.positionSide,
            "prd_name": self.dto.prd_name,
            "attach_name": self.get_attach_name()
        })
        self.prepareData.orderPack = odp
        self.prepareData.orders = [order_dto.convert_entity_to_dto(o) for o in ods]
        self.prepareData.currentPrice = self.tradeClient.get_last_price(self.dto.prd_name)
        return self

    def fuse(self) -> FuseResult:
        if not self.has_position():
            return FuseResult(result_type=FuseResultType.NO_POSITION)
        if not self.is_match_criteria():
            return FuseResult(result_type=FuseResultType.NO_CRITERIA)
        if self.is_up_to_date():
            return FuseResult(result_type=FuseResultType.UP_TO_DATE)
        close_orders = self.cancel_exist_orders()
        new_orders = self.post_fuse_orders()
        return FuseResult(result_type=FuseResultType.EXECUTED, closeOrders=close_orders, newOrders=new_orders)

    def has_position(self) -> bool:
        return position_utils.get_abs_amt(self.prepareData.position) > 0

    def cancel_exist_orders(self) -> List[OrderDto]:
        if not self.prepareData.orders:
            return list()
        return self.orderClient.clean_orders(symbol=self.dto.prd_name, currentOds=self.prepareData.orders)

    @abc.abstractmethod
    def get_attach_name(self) -> str:
        raise NotImplementedError('get_attach_name')

    @abc.abstractmethod
    def is_match_criteria(self) -> bool:
        raise NotImplementedError('is_match_criteria')

    @abc.abstractmethod
    def is_up_to_date(self) -> bool:
        raise NotImplementedError('is_up_to_date')

    @abc.abstractmethod
    def post_fuse_orders(self) -> [OrderDto]:
        raise NotImplementedError('post_fuse_orders')


class FixedStepAttach:

    def __init__(self, currentTopPrice: float, positionAmt: float):
        self.currentTopPrice: float = currentTopPrice
        self.positionAmt: float = positionAmt


class FixedStepFuseBuilder(BaseFuseBuilder[FixedStepFuseDto]):

    def get_attach_name(self) -> str:
        return 'FuseFixedStep'

    def _get_attach(self) -> FixedStepAttach:
        if not self.prepareData.orderPack:
            return None
        return FixedStepAttach(**self.prepareData.orderPack.get_attach())

    def is_match_criteria(self) -> bool:
        return True

    def is_up_to_date(self) -> bool:
        if not self._get_attach():
            return False
        attach = self._get_attach()
        if not comm_utils.is_similar(attach.positionAmt,
                                     position_utils.get_abs_amt(self.prepareData.position)):
            return False
        if self.is_manual_adjust_orders():
            return False
        if direction_utils.is_high_price(self.dto.positionSide, attach.currentTopPrice, self.prepareData.currentPrice):
            return True
        dif_price = abs(attach.currentTopPrice - self.prepareData.currentPrice)
        dif_rate = dif_price / self.dto.priceStep
        if dif_rate > self.dto.rebuildByPriceStepRate:
            return False
        return True

    @abc.abstractmethod
    def is_manual_adjust_orders(self) -> bool:
        raise NotImplementedError('is_manual_adjust_orders')

    def post_fuse_orders(self) -> [OrderDto]:
        ans: List[OrderDto] = list()
        post_count = self._get_step_count()
        price_qty_list: List[PriceQty] = self._gen_price_qty_list(post_count)
        for pq in price_qty_list:
            o_dto = self.orderClient.post_stop_market(prd_name=self.dto.prd_name, price=pq.price,
                                                      quantity=pq.quantity,
                                                      positionSide=self.dto.positionSide, tags=self.dto.tags)
            ans.append(o_dto)
        self._record_pack_info(ans)
        return ans

    def _record_pack_info(self, ods: List[OrderDto]):
        parameters = dict(self.dto.__dict__)
        parameters.pop("attach", None)
        parameters.pop("tags", None)
        od_pack_entity = OrderPack()
        od_pack_entity.set_tags(self.dto.tags)
        od_pack_entity.order_strategy = self.dto.fuseStrategy
        od_pack_entity.market_price = self.prepareData.currentPrice

        attach = FixedStepAttach(currentTopPrice=self.prepareData.currentPrice,
                                 positionAmt=position_utils.get_abs_amt(self.prepareData.position))

        od_pack_entity.set_attach(attach.__dict__)
        od_pack_entity.attach_name = self.get_attach_name()
        od_pack_entity.set_parameters(parameters)
        od_pack_entity.positionSide = self.dto.positionSide
        od_pack_entity.prd_name = self.dto.prd_name
        self.orderPackDao.create_by_orders(ods=ods, od_pack_entity=od_pack_entity)

    def _get_step_count(self):
        entryPrice = self.prepareData.position.entryPrice
        if direction_utils.is_high_price(self.dto.positionSide, self.prepareData.currentPrice, entryPrice):
            return self.dto.minCount
        dif_price = abs(self.prepareData.currentPrice - entryPrice)
        _count = math.ceil(dif_price / self.dto.priceStep)
        if _count >= self.dto.noLoseBaseCount:
            return _count
        return _count + self.dto.minCount

    def _gen_price_qty_list(self, count: int) -> List[PriceQty]:
        part_qty: float = position_utils.get_abs_amt(self.prepareData.position)
        per_qty: float = comm_utils.calc_proportional_first(sum=part_qty, rate=self.dto.proportionalRate,
                                                            n=count)
        priceQtyList: List[PriceQty] = list()
        for i in range(count):
            p = self._calc_fall_price(i)
            q = self._calc_proportional_amt(per_qty, i)
            priceQtyList.append(PriceQty(
                price=p,
                quantity=q
            ))
        return priceQtyList

    def _calc_proportional_amt(self, per_qty: float, i: int) -> float:
        num = self.dto.size - i if self.dto.proportionalReverse else i
        return per_qty * pow(self.dto.proportionalRate, num)

    def get_abc_clazz(self) -> object:
        return FixedStepFuseBuilder

    def _calc_fall_price(self, i):
        return direction_utils.plus_price_by_fixed(self.dto.positionSide, self.prepareData.currentPrice,
                                                   -self.dto.priceStep * (i + 1))


def gen_fuse_builder(session: Session, payload: dict) -> BaseFuseBuilder:
    strategy: str = payload.get('fuseStrategy')
    strategy: OrderStrategy = comm_utils.value_of_enum(OrderStrategy, strategy)
    if strategy == OrderStrategy.FUSE_FIXED_STEP:
        return exchange.gen_impl_obj(exchange_name=PayloadReqKey.exchange.get_val(payload),
                                     clazz=FixedStepFuseBuilder, session=session).init(
            FixedStepFuseDto(**payload))

    raise NotImplementedError(f'not Implemented {strategy} ')
