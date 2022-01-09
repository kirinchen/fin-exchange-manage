import abc
from abc import ABC
from typing import List

from sqlalchemy.orm import Session

from dto.position_dto import PositionDto, PositionFilter
from service.base_exchange_abc import BaseExchangeAbc
from service.product_dao import ProductDao
from utils import position_utils


class PositionClientService(BaseExchangeAbc, ABC):

    def __init__(self, exchange_name: str, session: Session):
        super().__init__(exchange_name, session)
        self.productDao: ProductDao = None

    def after_init(self):
        self.productDao = self.get_ex_obj(ProductDao)

    def get_abc_clazz(self) -> object:
        return PositionClientService

    @abc.abstractmethod
    def list_all(self) -> List[PositionDto]:
        raise NotImplementedError('list_all')

    def query(self, position_filter: PositionFilter) -> List[PositionDto]:
        return position_utils.filter_position(self.list_all(), position_filter)

    def find_one(self, symbol: str, positionSide: str) -> PositionDto:
        return position_utils.find_position_one(self.list_all(), symbol, positionSide)

    def get_max_order_amt(self, symbol: str, positionSide: str, price: float) -> float:
        pos = self.find_one(symbol, positionSide)
        return pos.maxNotionalValue / price

    @abc.abstractmethod
    def close(self, prd_name: str, positionSide: str, amount: float) -> any:
        raise NotImplementedError('close')
