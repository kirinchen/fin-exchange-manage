import importlib
import os
from typing import TypeVar

wd_path = os.path.dirname(__file__)

T = TypeVar("T")

wd_path = os.path.dirname(__file__)


def load_function(exchange: str, name: str) -> object:
    spec = importlib.util.spec_from_file_location("action", f"{wd_path}/{exchange}/{name}.py")
    foo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(foo)
    return foo.get_instance()
