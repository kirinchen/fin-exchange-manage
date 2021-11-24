import abc
from abc import ABC
from typing import TypeVar, Generic, Any

from sqlalchemy.orm import scoped_session, Session


class BaseExchangeAbc(ABC):

    def __init__(self, exchange: str, session: Session = None):
        self.exchange = exchange
        self.session: Session = session

    def after_init(self):
        pass

    @abc.abstractmethod
    def get_abc_clazz(self) -> object:
        raise NotImplementedError()


T = TypeVar('T')


class BaseDao(Generic[T], BaseExchangeAbc, ABC):

    @abc.abstractmethod
    def get_entity_clazz(self) -> T:
        raise NotImplementedError('get_entity_clazz')

    def get(self, pkid: Any) -> T:
        return self.session.query(self.get_entity_clazz()).get(pkid)

    def update(self, entity: T) -> T:
        self.session.merge(entity)
        self.session.flush()
        return entity

    def refresh_all(self):
        pass
