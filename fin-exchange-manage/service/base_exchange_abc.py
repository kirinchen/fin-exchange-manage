import abc
from abc import ABC
from datetime import datetime, timezone
from typing import TypeVar, Generic, Any

from sqlalchemy.orm import scoped_session, Session

import exchange
from model.comm import TimestampMixin

EX = TypeVar('E')


class BaseExchangeAbc(ABC):

    def __init__(self, exchange_name: str, session: Session):
        self.exchange_name = exchange_name
        self.session: Session = session

    def after_init(self):
        pass

    @abc.abstractmethod
    def get_abc_clazz(self) -> object:
        raise NotImplementedError()

    def get_ex_obj(self, ex: EX) -> EX:
        return exchange.gen_impl_obj(self.exchange_name, ex,
                                     self.session)


T = TypeVar('T')


class BaseDao(BaseExchangeAbc,Generic[T], ABC):

    @abc.abstractmethod
    def get_entity_clazz(self) -> T:
        raise NotImplementedError('get_entity_clazz')

    def get(self, pkid: Any) -> T:
        return self.session.query(self.get_entity_clazz()).get(pkid)

    def create(self, entity: T) -> T:
        if isinstance(entity, TimestampMixin):
            entity.created_at = datetime.now(tz=timezone.utc)
        self.session.add(entity)
        self.session.flush()
        return entity

    def update(self, entity: T) -> T:
        if isinstance(entity, TimestampMixin):
            entity.updated_at = datetime.now(tz=timezone.utc)
        self.session.merge(entity)
        self.session.flush()

        return entity

    def refresh_all(self):
        pass
