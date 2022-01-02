from typing import List

from model import Order
from service.base_exchange_abc import BaseDao
from utils import comm_utils


class OrderDao(BaseDao):

    def get_abc_clazz(self) -> object:
        return OrderDao

    def get_entity_clazz(self) -> Order:
        return Order

    def create(self, entity: Order) -> Order:
        entity.uid = comm_utils.random_chars(12)
        entity.exchange = self.exchange_name
        return super(OrderDao, self).create(entity)