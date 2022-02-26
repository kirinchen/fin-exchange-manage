from typing import List

from maicoin_max.client import Client

from dto import order_dto
from dto.position_dto import PositionDto
from exchange.maicoin_max import gen_request_client
from service.order_client_service import OrderClientService
from service.order_dao import OrderDao
from service.position_client_service import PositionClientService
from service.wallet_client_service import WalletClientService
from utils import position_utils


class MaxPositionClientService(PositionClientService):

    def __init__(self, **kwargs):
        super(MaxPositionClientService, self).__init__(**kwargs)
        self.client: Client = gen_request_client()
        self.orderDao: OrderDao = None
        self.walletClient: WalletClientService = None

    def after_init(self):
        self.orderDao = self.get_ex_obj(OrderDao)
        self.walletClient = self.get_ex_obj(WalletClientService)

    def list_all(self) -> List[PositionDto]:
        order_entitys = self.orderorderDao.list_filled()
        order_dtos = [order_dto.convert_entity_to_dto(e) for e in order_entitys]
        position_utils.get_by_orders # TODO: check
        return None
        # result: List[Position] = self.client.get_position()
        # return [binance_utils.convert_position_dto(op) for op in result]

    def close(self, prd_name: str, positionSide: str, amount: float) -> any:
        pass


def get_impl_clazz() -> MaxPositionClientService:
    return MaxPositionClientService
