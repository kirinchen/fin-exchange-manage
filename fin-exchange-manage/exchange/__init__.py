import importlib
import os
from typing import TypeVar, List, Dict

from service.base_service import BaseService

wd_path = os.path.dirname(__file__)

T = TypeVar("T")

wd_path = os.path.dirname(__file__)


def load_function(exchange: str, name: str) -> object:
    spec = importlib.util.spec_from_file_location("action", f"{wd_path}/{exchange}/{name}.py")
    foo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(foo)
    return foo.get_instance()


_service_map: Dict[str, Dict[object, BaseService]] = dict()


def load_all_service():
    wd_path = os.path.dirname(__file__)
    ex_dirs: List[str] = next(os.walk(wd_path), (None, [], None))[1]  # [] if no file
    for exchange_name in ex_dirs:
        path = f'{wd_path}/{exchange_name}/__service/'
        _service_map[exchange_name] = dict()
        _load_exchange_all_service(exchange_name, path)


def _load_exchange_all_service(exchange_name: str, exchange_path: str):
    service_filenames: List[str] = next(os.walk(exchange_path), (None, None, []))[2]  # [] if no file
    for service_filename in service_filenames:
        path = f'{exchange_path}/{service_filename}'
        spec = importlib.util.spec_from_file_location("action", path)
        foo = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(foo)
        service_clazz: BaseService = foo.get_service_clazz()
        service_instance: BaseService = service_clazz(exchange_name)
        this_dict = _service_map[exchange_name]
        this_dict[service_instance.get_abc_clazz()] = service_instance


S = TypeVar("S", bound=BaseService)


def get_service(exchange_name: str, clazz: S) -> S:
    return _service_map[exchange_name][clazz]
