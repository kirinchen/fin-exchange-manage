from typing import List

from sqlalchemy.orm import Session

from binance_f import RequestClient
from binance_f.model import Position
from dto.position_dto import PositionDto
from exchange.binance import gen_request_client, binance_utils
from service.position_client_service import PositionClientService


class BinancePositionClientService(PositionClientService):

    def __init__(self, exchange_name: str, session: Session = None):
        super(BinancePositionClientService, self).__init__(exchange_name, session)
        self.client: RequestClient = gen_request_client()

    def list_all(self) -> List[PositionDto]:
        result: List[Position] = self.client.get_position()
        return [binance_utils.convert_position_dto(op) for op in result]


def get_impl_clazz() -> BinancePositionClientService:
    return BinancePositionClientService
