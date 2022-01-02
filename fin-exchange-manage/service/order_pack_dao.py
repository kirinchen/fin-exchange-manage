from typing import List

from sqlalchemy.orm import Session

from dto import order_dto
from model import Order
from model.order_pack import OrderPack
from service.base_exchange_abc import BaseDao, BaseExchangeAbc
from service.order_dao import OrderDao
from utils import comm_utils, order_utils


class OrderPackDao(BaseDao):

    def __init__(self, exchange_name: str, session: Session = None):
        super(OrderPackDao, self).__init__(exchange_name, session)
        self.orderDao: OrderDao = None

    def after_init(self):
        self.orderDao = self.get_ex_obj(OrderDao)

    def get_abc_clazz(self) -> object:
        return OrderPackDao

    def create(self, entity: OrderPack) -> OrderPack:
        entity.uid = comm_utils.random_chars(12)
        entity.exchange = self.exchange_name
        return super(OrderPackDao, self).create(entity)

    def create_by_orders(self, od_pack_entity: OrderPack, ods: List[Order]) -> OrderPack:
        if len(ods) <= 0:
            return

        self.create(od_pack_entity)
        for od in ods:
            od_entity = order_utils.convert_to_model(dto=od, exchange=self.exchange_name, order_strategy=strategy)
            od_entity.pack_uid = od_pack_entity.uid
            od_entity.set_tags(tags)
            self.orderDao.create(od_entity)

    def get_entity_clazz(self) -> OrderPack:
        return OrderPack