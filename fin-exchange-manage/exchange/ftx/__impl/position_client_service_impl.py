from typing import List

from binance_f import RequestClient
from binance_f.model import Position
from sqlalchemy.orm import Session

from dto.position_dto import PositionDto
from exchange.binance import gen_request_client, binance_utils
from service.position_client_service import PositionClientService


class FTXPositionClientService(PositionClientService):

    def __init__(self, **kwargs):
        super(FTXPositionClientService, self).__init__(**kwargs)
        self.client: RequestClient = gen_request_client()

    def list_all(self) -> List[PositionDto]:
        result: List[Position] = self.client.get_position()
        return [binance_utils.convert_position_dto(op) for op in result]

    def close(self, prd_name: str, positionSide: str, amount: float) -> any:
        pass


def get_impl_clazz() -> FTXPositionClientService:
    return FTXPositionClientService
