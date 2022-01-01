from typing import List

from model import Order
from service.base_exchange_abc import BaseDao


class OrderDao(BaseDao):

    def get_abc_clazz(self) -> object:
        return OrderDao

    def get_entity_clazz(self) -> Order:
        return Order
