from typing import List

from maicoin_max.client import Client

from dto import order_dto
from dto.order_dto import OrderDto
from dto.position_dto import PositionDto
from dto.wallet_dto import WalletDto
from exchange.maicoin_max import gen_request_client, max_utils
from model.init_data import init_item
from service.market_client_sevice import MarketClientService
from service.order_client_service import OrderClientService
from service.order_dao import OrderDao
from service.position_client_service import PositionClientService
from service.wallet_client_service import WalletClientService
from utils import position_utils, order_utils
from utils.order_utils import OrderFilter
from utils.wallet_utils import WalletFilter


class MaxPositionClientService(PositionClientService):

    def __init__(self, **kwargs):
        super(MaxPositionClientService, self).__init__(**kwargs)
        self.client: Client = gen_request_client()
        self.orderDao: OrderDao = None
        self.walletClient: WalletClientService = None
        self.marketClient: MarketClientService = None

    def after_init(self):
        self.orderDao = self.get_ex_obj(OrderDao)
        self.walletClient = self.get_ex_obj(WalletClientService)
        self.marketClient = self.get_ex_obj(MarketClientService)

    def list_all(self) -> List[PositionDto]:
        order_entitys = self.orderDao.list_filled()
        order_dtos = [order_dto.convert_entity_to_dto(e) for e in order_entitys]
        wallet_dtos = self.walletClient.query(
            WalletFilter(amount_exist=True, not_symbol=init_item.get_instance().twd.symbol))
        for w_dto in wallet_dtos:
            self._calc_position(w_dto=w_dto, orders=order_dtos)

        # order_utils.get_entry_price_by_orders()
        return None
        # result: List[Position] = self.client.get_position()
        # return [binance_utils.convert_position_dto(op) for op in result]

    def _calc_position(self, w_dto: WalletDto, orders: List[OrderDto]) -> PositionDto:
        this_ods = order_utils.filter_order(orders, OrderFilter(symbol=max_utils.fix_twd_prd_name(w_dto.symbol)))

    def close(self, prd_name: str, positionSide: str, amount: float) -> any:
        pass


def get_impl_clazz() -> MaxPositionClientService:
    return MaxPositionClientService
