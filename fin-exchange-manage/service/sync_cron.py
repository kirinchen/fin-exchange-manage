from abc import ABC
from typing import TypeVar

from sqlalchemy.orm import Session

import exchange
from infra import database
from service.base_exchange_abc import BaseExchangeAbc, BaseDao
from service.product_dao import ProductDao


class SyncCron(BaseExchangeAbc, ABC):

    def init_bind_load(self):
        with database.session_scope() as session:
            session: Session
            self.sync_for_dao(ProductDao, session)

    def sync_for_dao(self, dao_clazz: BaseDao, session: Session):
        exchange.gen_impl_obj(self.exchange, dao_clazz, session).refresh_all()

    def get_abc_clazz(self) -> object:
        return SyncCron


def init_bind_all():
    for ex in exchange.list_exchange_name():
        sc: SyncCron = exchange.gen_impl_obj(ex, SyncCron)
        sc.init_bind_load()
