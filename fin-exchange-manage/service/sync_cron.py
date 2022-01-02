import abc
from abc import ABC
from datetime import datetime, timedelta
from typing import List

from sqlalchemy.orm import Session

import exchange
from dto.order_dto import OrderDto
from infra import database
from model import Product, Order
from service.base_exchange_abc import BaseExchangeAbc
from service.order_client_service import OrderClientService
from service.order_dao import OrderDao
from service.product_dao import ProductDao
from utils import order_utils

_last_order_sync_at: datetime = datetime.utcnow() + timedelta(hours=-8)


class SyncCron(BaseExchangeAbc, ABC):

    def __init__(self, exchange_name: str, session: Session):
        super().__init__(exchange_name, session)
        self.orderDao: OrderDao = None
        self.orderClientService: OrderClientService = None

    def after_init(self):
        self.orderDao = self.get_ex_obj(OrderDao)
        self.orderClientService = self.get_ex_obj(OrderClientService)

    def init_bind_load(self):
        self.sync_all_product()

    def sync_all_product(self):
        p_dao: ProductDao = self.get_ex_obj(ProductDao)
        ps: List[Product] = p_dao.list_by_this_exchange()
        for p in ps:
            self.sync_product(p, p_dao)

    def sync_orders(self, prd_name: str) -> dict:
        st = int(_last_order_sync_at.timestamp() * 1000)
        ods: List[OrderDto] = self.orderClientService.list_all_order(prd_name=prd_name,
                                                                     startTime=st)
        ex_id_list = [str(o.orderId) for o in ods]
        exist_orders: List[Order] = self.orderDao.list_in_exchange_id_list(ex_id_list)
        exist_count = 0
        new_count = 0
        for od in ods:
            eol = [eo for eo in exist_orders if eo.exchangeOrderId == str(od.orderId)]
            if len(eol) > 0:
                exist_count += 1
                eo = eol[0]
                self.orderDao.update(order_utils.merge_dto_entity(od, eo))
            else:
                new_count += 1
                self.orderDao.create(order_utils.convert_to_model(dto=od, exchange=self.exchange_name))
        _set_last_order_sync_at_now()
        return {
            'exist': exist_count,
            'new': new_count
        }

    @abc.abstractmethod
    def sync_product(self, p: Product, product_dao: ProductDao):
        raise NotImplementedError('sync_product')

    def get_abc_clazz(self) -> object:
        return SyncCron


def _set_last_order_sync_at_now():
    global _last_order_sync_at
    _last_order_sync_at = datetime.utcnow


def init_bind_all():
    with database.session_scope() as session:
        for ex in exchange.list_exchange_name():
            sc: SyncCron = exchange.gen_impl_obj(ex, SyncCron, session)
            sc.init_bind_load()
