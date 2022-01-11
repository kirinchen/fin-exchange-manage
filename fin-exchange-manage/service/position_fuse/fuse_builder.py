import abc
from abc import ABC
from enum import Enum
from typing import TypeVar, Generic, List

from sqlalchemy.orm import Session

from dto import order_dto
from dto.fuse_dto import BaseFuseDto, FixedStepFuseDto
from dto.order_dto import OrderDto
from dto.position_dto import PositionDto
from model import OrderPack
from service.base_exchange_abc import BaseExchangeAbc
from service.order_pack_dao import OrderPackDao
from service.position_client_service import PositionClientService
from service.trade_client_service import TradeClientService
from utils import position_utils, comm_utils


class FuseResultType(Enum):
    NO_POSITION = 'NO_POSITION'
    NO_CRITERIA = 'NO_CRITERIA'
    UP_TO_DATE = 'UP_TO_DATE'


class FuseResult:

    def __init__(self, result_type: FuseResultType):
        self.resultType = result_type


class FusePrepareData:

    def __init__(self):
        self.position: PositionDto = None
        self.orderPack: OrderPack = None
        self.orders: List[OrderDto] = None
        self.currentPrice: float = None


T = TypeVar('T', bound=BaseFuseDto)


class BaseFuseBuilder(BaseExchangeAbc, Generic[T], ABC):

    def __init__(self, exchange_name: str, session: Session):
        super().__init__(exchange_name, session)
        self.prepareData: FusePrepareData = None
        self.dto: T = None
        self.positionClient: PositionClientService = None
        self.orderPackDao: OrderPackDao = None
        self.tradeClient: TradeClientService = None

    def after_init(self):
        self.positionClient = self.get_ex_obj(PositionClientService)
        self.orderPackDao = self.get_ex_obj(OrderPackDao)
        self.tradeClient = self.get_ex_obj(TradeClientService)

    def init(self, dto: T, fuse_prepare_data=FusePrepareData()):
        self.dto = dto
        self.prepareData: FusePrepareData = fuse_prepare_data
        self.prepareData.position = self.positionClient.find_one(self.dto.symbol, self.dto.positionSide)
        odp, ods = self.orderPackDao.last({
            "exchange": self.exchange_name,
            "positionSide": self.dto.positionSide,
            "prd_name": self.prd_name,
            "attach_name": self.get_attach_name()
        })
        self.prepareData.orderPack = odp
        self.prepareData.orders = [order_dto.convert_entity_to_dto(o) for o in ods]
        self.prepareData.currentPrice = self.tradeClient.get_last_price(self.dto.prd_name)

    def fuse(self) -> FuseResult:
        if not self.has_position():
            return FuseResult(result_type=FuseResultType.NO_POSITION)
        if not self.is_match_criteria():
            return FuseResult(result_type=FuseResultType.NO_CRITERIA)
        if self.is_up_to_date():
            return FuseResult(result_type=FuseResultType.UP_TO_DATE)

    def has_position(self) -> bool:
        return position_utils.get_abs_amt(self.position) > 0

    @abc.abstractmethod
    def get_attach_name(self) -> str:
        raise NotImplementedError('get_attach_name')

    @abc.abstractmethod
    def is_match_criteria(self) -> bool:
        raise NotImplementedError('is_match_criteria')

    @abc.abstractmethod
    def is_up_to_date(self) -> bool:
        raise NotImplementedError('is_up_to_date')


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
                                     position_utils.get_abs_amt(self.prepareData.position.positionAmt)):
            return False

        return True

    def get_abc_clazz(self) -> object:
        return FixedStepFuseBuilder
