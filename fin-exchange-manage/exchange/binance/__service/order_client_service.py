from typing import List

from dto.order_dto import OrderDto
from service.order_client_service import OrderClientService


class BinanceOrderClientService(OrderClientService):

    def list_all_order(self, symbol: str, orderId: int = None, startTime: int = None, endTime: int = None,
                       limit: int = None) -> List[OrderDto]:
        pass


def get_service_clazz() -> BinanceOrderClientService:
    return BinanceOrderClientService
