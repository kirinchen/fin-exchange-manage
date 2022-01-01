from model import Order
from model.order_batch import OrderBatch
from service.base_exchange_abc import BaseDao
from utils import comm_utils


class OrderBatchDao(BaseDao):

    def get_abc_clazz(self) -> object:
        return OrderBatchDao

    def create(self, entity: Order) -> Order:
        entity.uid = comm_utils.random_chars(12)
        return super(OrderBatchDao, self).create(entity)

    def get_entity_clazz(self) -> OrderBatch:
        return OrderBatch
