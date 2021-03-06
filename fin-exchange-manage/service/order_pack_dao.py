from typing import List

from sqlalchemy import desc, Column
from sqlalchemy.orm import Session, Query

from dto import order_dto
from dto.order_dto import OrderPackQueryDto, OrderDto
from model import Order
from model.order_pack import OrderPack
from service.base_exchange_abc import BaseDao, BaseExchangeAbc
from service.order_dao import OrderDao
from utils import comm_utils, order_utils

DTO_IN_FIELD_SUBFIX = '_IN'


class OrderPackDao(BaseDao[OrderPack]):

    def __init__(self, **kwargs):
        super(OrderPackDao, self).__init__(**kwargs)
        self.orderDao: OrderDao = None

    def after_init(self):
        self.orderDao = self.get_ex_obj(OrderDao)

    def get_abc_clazz(self) -> object:
        return OrderPackDao

    def create(self, entity: OrderPack) -> OrderPack:
        entity.uid = comm_utils.random_chars(12)
        entity.exchange = self.exchange_name
        return super(OrderPackDao, self).create(entity)

    def query_by_dict(self, d: dict) -> Query:
        in_map = dict()
        for k, v in dict(d).items():
            if k.endswith(DTO_IN_FIELD_SUBFIX):
                del d[k]
                in_map[k] = v
        ans: Query = self.gen_query().filter_by(**d)
        for ink, inv in in_map.items():
            col_name: str = ink.replace(DTO_IN_FIELD_SUBFIX, '')
            col: Column = self.get_column(col_name)
            ans = ans.filter(col.in_(inv))

        return ans

    def last(self, d: dict) -> (OrderPack, List[Order]):
        entity: OrderPack = self.query_by_dict(d).order_by(desc(OrderPack.created_at)).first()
        if not entity:
            return entity, list()
        orders: List[Order] = self.orderDao.list_by_pack(entity.uid)
        return entity, orders

    def create_by_orders(self, od_pack_entity: OrderPack, ods: List[Order]) -> OrderPack:
        if len(ods) <= 0:
            return
        self.create(od_pack_entity)
        for od in ods:
            if not od:
                continue
            od_entity = order_utils.convert_to_model(dto=od, exchange=self.exchange_name, pack_uid=od_pack_entity.uid,
                                                     order_strategy=od_pack_entity.order_strategy)
            od_entity.set_tags(od_pack_entity.tags)
            self.orderDao.create(od_entity)

    def get_entity_clazz(self) -> OrderPack:
        return OrderPack
