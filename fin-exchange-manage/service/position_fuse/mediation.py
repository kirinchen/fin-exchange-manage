import abc
from enum import Enum
from typing import List, TypeVar, Generic

from sqlalchemy.orm import Session

from dto.account_dto import AccountDto
from dto.order_dto import OrderDto
from dto.position_dto import PositionDto
from model import exchange
from rest import account
from service.order_client_service import OrderClientService
from service.position_client_service import PositionClientService
from service.position_fuse.stop_guaranteed import StopGuaranteedDto
from service.position_fuse.stop_loss import StopLossDto, StopLoss
from service.trade_client_service import TradeClientService
from utils import position_utils, order_utils
from utils.order_utils import OrdersInfo


class StopMediationDto:

    def __init__(self, symbol: str, positionSide: str, tags: List[str], stopLoss: dict, stopGuaranteed: dict):
        self.symbol: str = symbol
        self.positionSide: str = positionSide
        self.tags: List[str] = tags
        self._apply_default_fields(stopLoss)
        self.stopLoss = StopLossDto(**stopLoss)
        self._apply_default_fields(stopGuaranteed)
        self.stopGuaranteed = StopGuaranteedDto(**stopGuaranteed)

    def _apply_default_fields(self, dto: dict):
        dto.update({
            'symbol': self.symbol,
            'positionSide': self.positionSide,
            'tags': self.tags
        })


class StopState(Enum):
    NO_POS = 'NO_POS'
    LOSS = 'LOSS'
    GUARANTEED = 'GATE'
    PROFIT = 'PROF'


class StopResult:

    def __init__(self, stopState: StopState, orders: List[OrderDto] = list(), active: bool = False,
                 noActiveMsg: str = None,
                 up_to_date: bool = False):
        self.active = active
        self.stopState: str = stopState.value
        self.orders: List[OrderDto] = orders
        self.noActiveMsg: str = noActiveMsg
        self.up_to_date: bool = up_to_date


class StopDto(metaclass=abc.ABCMeta):

    def __init__(self, symbol: str, positionSide: str, tags: List[str]):
        self.symbol: str = symbol
        self.positionSide: str = positionSide
        self.tags: List[str] = tags


T = TypeVar('T', bound=StopDto)


class Stoper(Generic[T], metaclass=abc.ABCMeta):

    def __init__(self, exchange_name: str, session: Session, state: StopState, dto: T):
        self.session = session
        self.exchange_name = exchange_name
        self.dto: T = dto
        self.state: StopState = state
        self.position_client: PositionClientService = exchange.gen_impl_obj(self.exchange_name, PositionClientService,
                                                                            self.session)
        self.tradeClientService: TradeClientService = exchange.gen_impl_obj(self.exchange_name, TradeClientService,
                                                                            self.session)
        self.orderClientService: OrderClientService = exchange.gen_impl_obj(self.exchange_name, OrderClientService,
                                                                            self.session)
        self.position: PositionDto = self.get_current_position()
        self.no_position = position_utils.get_abs_amt(self.position) <= 0
        self.tags = self._setup_tags(list(dto.tags))
        if self.no_position:
            return
        self.currentStopOrdersInfo: OrdersInfo = None
        self.lastPrice: float = None

    def load_vars(self):
        if self.no_position:
            raise TypeError('no position')
        all_orders = self.orderClientService.list_all_order(symbol=self.dto.symbol)
        self.currentStopOrdersInfo = order_utils.get_current_new_stop_orders(all_orders,
                                                                             self.client,
                                                                             self.position)
        self.lastPrice: float = self.tradeClientService.get_last_fall_price(symbol=self.dto.symbol,
                                                                            positionSide=self.dto.positionSide)

    def _setup_tags(self, tags: List[str]) -> List[str]:
        tags.append(self.state.value)
        return tags

    def get_current_position(self) -> PositionDto:
        return self.position_client.find_one(self.dto.symbol, self.dto.positionSide)

    def get_account(self) -> AccountDto:
        return account.info.get.invoke(self.exchange_name)

    def is_conformable(self) -> bool:
        """
        表示有達到該 range 的進入門檻
        """
        return not self.no_position

    @abc.abstractmethod
    def is_up_to_date(self) -> bool:
        return NotImplemented

    @abc.abstractmethod
    def clean_old_orders(self) -> List[OrderDto]:
        return NotImplemented

    @abc.abstractmethod
    def stop(self) -> StopResult:
        return NotImplemented

    def run(self) -> StopResult:
        if self.no_position:
            return StopResult(stopState=self.state, noActiveMsg='no_position')
        if not self.is_conformable():
            return StopResult(stopState=self.state, noActiveMsg='not is_conformable')
        if self.is_up_to_date():
            return StopResult(stopState=self.state, active=True, up_to_date=True)
        self.clean_old_orders()
        return self.stop()


class StopMediation:

    def __init__(self, dto: StopMediationDto):
        self.dto: StopMediationDto = dto
        self.stopLoss = StopLoss(client=self.client, dto=self.dto.stopLoss)
        self.stopGuaranteed = StopGuaranteed(client=self.client, dto=self.dto.stopGuaranteed)

    def stop(self) -> List[StopResult]:
        if self.stopGuaranteed.no_position:
            return [StopResult(stopState=StopState.NO_POS, noActiveMsg='no_position')]
        return self._stop_each([self.stopGuaranteed, self.stopLoss])

    def _stop_each(self, stops: List[Stoper]) -> List[StopResult]:
        no_stop_results: List[StopResult] = list()
        for stop in stops:
            stop.load_vars()
            stop_result: StopResult = stop.run()
            no_stop_results.append(stop_result)
            if stop_result.active:
                break

        return no_stop_results
