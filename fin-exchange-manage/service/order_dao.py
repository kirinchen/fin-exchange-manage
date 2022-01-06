from typing import List

from model import Order
from service.base_exchange_abc import BaseDao
from utils import comm_utils


class OrderDao(BaseDao[Order]):

    def get_abc_clazz(self) -> object:
        return OrderDao

    def get_entity_clazz(self) -> Order:
        return Order

    def create(self, entity: Order) -> Order:
        entity.uid = comm_utils.random_chars(12)
        entity.exchange = self.exchange_name
        return super(OrderDao, self).create(entity)

    def list_in_exchange_id_list(self, id_list: List[str]) -> List[Order]:
        return self.session.query(Order).filter(Order.exchange == self.exchange_name).filter(
            Order.exchangeOrderId.in_(id_list)).all()

    def list_by_pack(self, pack_uid: str) -> List[Order]:
        return self.gen_query().filter(Order.pack_uid == pack_uid).all()
