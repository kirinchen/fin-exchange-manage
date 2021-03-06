import abc
from enum import Enum
from typing import List, TypeVar, Generic

from sqlalchemy.orm import Session

from dto.account_dto import AccountDto
from dto.order_dto import OrderDto
from dto.position_dto import PositionDto
from dto.wallet_dto import WalletDto
from infra.enums import OrderStatus
from model import Product
from rest import account
from service.base_exchange_abc import BaseExchangeAbc
from service.order_client_service import OrderClientService
from service.position_client_service import PositionClientService
from service.position_fuse import dtos
from service.product_dao import ProductDao
from service.trade_client_service import TradeClientService
from service.wallet_client_service import WalletClientService
from utils import position_utils, order_utils, direction_utils
from utils.order_utils import OrdersInfo, OrderFilter
from utils.wallet_utils import WalletFilter

T = TypeVar('T', bound=dtos.StopDto)


class Stoper(Generic[T], BaseExchangeAbc, metaclass=abc.ABCMeta):

    def __init__(self, state: dtos.StopState, **kwargs):
        super(Stoper, self).__init__(**kwargs)
        self.dto: T = None
        self.state: dtos.StopState = state
        self.position_client: PositionClientService = None
        self.productDao: ProductDao = None
        self.tradeClientService: TradeClientService = None
        self.orderClientService: OrderClientService = None
        self.walletClientService: WalletClientService = None
        self.position: PositionDto = None
        self.no_position: bool = None
        self.tags: List[str] = None
        self.currentStopOrdersInfo: OrdersInfo = None
        self.lastPrice: float = None
        self.product: Product = None

    def after_init(self):
        self.position_client: PositionClientService = self.get_ex_obj(PositionClientService)
        self.productDao: ProductDao = self.get_ex_obj(ProductDao)
        self.tradeClientService: TradeClientService = self.get_ex_obj(TradeClientService)
        self.orderClientService: OrderClientService = self.get_ex_obj(OrderClientService)
        self.walletClientService: WalletClientService = self.get_ex_obj(WalletClientService)

    def init(self, dto: T) -> object:
        self.dto: T = dto
        self.position: PositionDto = self.get_current_position()
        self.no_position = position_utils.get_abs_amt(self.position) <= 0
        self.tags = self._setup_tags(list(dto.tags))
        self.product: Product = self.productDao.get_by_prd_name(self.dto.symbol)
        return self

    def load_vars(self, all_orders: List[OrderDto]):
        if self.no_position:
            raise TypeError('no position')
        allStopOrders = order_utils.get_current_new_stop_orders(all_orders,
                                                                self.dto.symbol,
                                                                self.position.positionSide)
        self.currentStopOrdersInfo = order_utils.filter_order(allStopOrders.orders,
                                                              OrderFilter(tags=[self.state.value]))
        self.lastPrice: float = self.tradeClientService.get_last_fall_price(symbol=self.dto.symbol,
                                                                            positionSide=self.dto.positionSide)

    def _setup_tags(self, tags: List[str]) -> List[str]:
        tags.append(self.state.value)
        return tags

    def get_current_position(self) -> PositionDto:
        return self.position_client.find_one(self.dto.symbol, self.dto.positionSide)

    def get_wallet(self) -> WalletDto:
        return self.walletClientService.get_one(WalletFilter(prd_name=self.dto.symbol))

    def is_conformable(self) -> bool:
        """
        ?????????????????? range ???????????????
        """
        return not self.no_position

    @abc.abstractmethod
    def is_up_to_date(self) -> bool:
        return NotImplemented

    @abc.abstractmethod
    def clean_old_orders(self) -> List[OrderDto]:
        return NotImplemented

    @abc.abstractmethod
    def stop(self) -> dtos.StopResult:
        return NotImplemented

    def run(self) -> dtos.StopResult:
        if self.no_position:
            return dtos.StopResult(stopState=self.state, noActiveMsg='no_position')
        if not self.is_conformable():
            return dtos.StopResult(stopState=self.state, noActiveMsg='not is_conformable')
        if self.is_up_to_date():
            return dtos.StopResult(stopState=self.state, active=True, up_to_date=True)
        self.clean_old_orders()
        return self.stop()
