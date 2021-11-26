import abc
from abc import ABC
from typing import TypeVar, List

from sqlalchemy.orm import Session

import exchange
from infra import database
from model import Product
from service.base_exchange_abc import BaseExchangeAbc, BaseDao
from service.product_dao import ProductDao


class SyncCron(BaseExchangeAbc, ABC):

    def init_bind_load(self):
        with database.session_scope() as session:
            session: Session
            self.sync_all_product(session)

    def sync_all_product(self, session: Session):
        p_dao: ProductDao = self.get_ex_obj(ProductDao)
        ps: List[Product] = p_dao.list_by_this_exchange()
        for p in ps:
            self.sync_product(p, p_dao)

    @abc.abstractmethod
    def sync_product(self, p: Product, product_dao: ProductDao):
        raise NotImplementedError('sync_product')

    def get_abc_clazz(self) -> object:
        return SyncCron


def init_bind_all():
    with database.session_scope() as session:
        for ex in exchange.list_exchange_name():
            sc: SyncCron = exchange.gen_impl_obj(ex, SyncCron, session)
            sc.init_bind_load()
