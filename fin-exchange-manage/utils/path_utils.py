import os
from typing import List

from rest.proxy_controller import PayloadReqKey

REST_DIR = 'rest'
EXCHANGE_IMPL_FILE_SUFFIX = '_impl.py'


def get_rest_name(_file_: str) -> str:
    wd_path = os.path.abspath(_file_)

    ans: List[str] = list()
    ps: List[str] = wd_path.split(os.sep)
    start = False
    for p in ps:
        if start:
            ans.append(p)
        if p == REST_DIR:
            start = True

    return '/'.join(ans).replace('.py', '')


def get_rest_req_dict(exchange: str, _file_: str) -> dict:
    return {
        PayloadReqKey.name.value: get_rest_name(_file_),
        PayloadReqKey.exchange.value: exchange
    }


def get_exchange_impl_dir(wd_path: str, exchange_name: str) -> str:
    return f'{wd_path}/{exchange_name}/__impl/'
