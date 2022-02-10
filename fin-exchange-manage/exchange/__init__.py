import importlib
import os
from typing import TypeVar, List, Dict

from sqlalchemy.orm import Session

from service.base_exchange_abc import BaseExchangeAbc
from utils import path_utils

wd_path = os.path.dirname(__file__)

T = TypeVar("T")

wd_path = os.path.dirname(__file__)


def load_function(exchange: str, name: str) -> object:
    spec = importlib.util.spec_from_file_location("action", f"{wd_path}/{exchange}/{name}.py")
    foo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(foo)
    return foo.get_instance()


_impl_obj_map: Dict[str, Dict[object, BaseExchangeAbc]] = dict()


def list_exchange_name() -> List[str]:
    ans: List[str] = next(os.walk(wd_path), (None, [], None))[1]  # [] if no file
    return [x for x in ans if not (x.startswith('_') or x.endswith('_'))]


def load_all_service():
    ex_dirs: List[str] = list_exchange_name()
    for exchange_name in ex_dirs:
        path = path_utils.get_exchange_impl_dir(wd_path, exchange_name)
        _impl_obj_map[exchange_name] = dict()
        _load_exchange_all_service(exchange_name, path)


def _load_exchange_all_service(exchange_name: str, exchange_path: str):
    service_filenames: List[str] = next(os.walk(exchange_path), (None, None, []))[2]  # [] if no file
    _load_exchange_by_service_names(exchange_name, service_filenames, exchange_path)
    dirs: List[str] = next(os.walk(exchange_path), (None, [], None))[1]  # [] if no file
    for d in dirs:
        if d.startswith("_"):
            continue
        _load_exchange_all_service(exchange_name, f'{exchange_path}/{d}')


def _load_exchange_by_service_names(exchange_name: str, service_filenames: List[str], exchange_path: str):
    for service_filename in service_filenames:
        if not service_filename.endswith(path_utils.EXCHANGE_IMPL_FILE_SUFFIX):
            continue
        path = f'{exchange_path}/{service_filename}'
        print(f'path={path} load...')
        spec = importlib.util.spec_from_file_location("action", path)
        foo = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(foo)
        service_clazz: BaseExchangeAbc = foo.get_impl_clazz()
        service_instance: BaseExchangeAbc = service_clazz(exchange_name=exchange_name, session=None)
        this_dict = _impl_obj_map[exchange_name]
        this_dict[service_instance.get_abc_clazz()] = service_clazz


S = TypeVar("S", bound=BaseExchangeAbc)


def gen_impl_obj(exchange_name: str, clazz: S, session: Session,**kwargs) -> S:
    service_clazz = _impl_obj_map[exchange_name][clazz]
    ans = service_clazz(exchange_name=exchange_name, session=session)
    ans.after_init()
    return ans
