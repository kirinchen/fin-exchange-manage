import importlib
import os
from abc import ABC, abstractmethod
from typing import Dict, Generic, List, TypeVar

from sqlalchemy.orm import scoped_session

from infra import database

T = TypeVar("T")


class DataInit(ABC, Generic[T]):

    @abstractmethod
    def get_clazz(self) -> T:
        raise NotImplementedError('not impl')

    @abstractmethod
    def gen_data(self) -> List[T]:
        raise NotImplementedError('not impl')

    def save_all(self):
        with database.session_scope() as session:
            session: scoped_session = session
            session.query(self.get_clazz()).delete()
            for e in self.gen_data():
                session.add(e)
                session.flush()


def init_all_data():
    wd_path = os.path.dirname(__file__)
    filenames: List[str] = next(os.walk(wd_path), (None, None, []))[2]  # [] if no file
    for filename in filenames:
        if not filename.startswith('init_'):
            continue
        path: str = f"{wd_path}/{filename}"
        spec = importlib.util.spec_from_file_location("action", path)
        foo = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(foo)
        initer: DataInit = foo.get_instance()
        initer.save_all()
