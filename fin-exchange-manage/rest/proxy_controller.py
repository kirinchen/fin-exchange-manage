import json
import os
from contextlib import contextmanager
from datetime import datetime
from enum import Enum
import logging
from typing import Any

from flask import Flask, Response
from flask import request

import config
from binance_f import RequestClient, SubscriptionClient

import importlib.util

from utils import comm_utils

api_key = config.env('api-key')


class PayloadReqKey(Enum):
    name = 'name'
    exchange = 'exchange'
    apiKey = '__bzk_api_key'
    exchange_account = 'exchange_account'  # 如果沒有指定就是 load default 各自 impl 要各自實作

    @classmethod
    def values(cls):
        ans = [e for e in PayloadReqKey]
        return ans

    @classmethod
    def clean_default_keys(cls, payload: dict):
        for k in PayloadReqKey.values():
            if k.value in payload:
                del payload[k.value]

    def get_val(self, payload: dict) -> Any:
        return payload.get(self.value)


app = Flask(__name__)


@app.route('/')
def index():
    return f"Hello, World! BA"


@app.route('/log')
def log():
    filepath = '/tmp/{:%Y-%m-%d}.log'.format(datetime.now())
    enc = 'utf-8'
    with open(filepath, encoding=enc) as fp:
        ctn = fp.read()
        return ctn


@app.route('/test')
def test():
    return {
        "fin-measurement": config.env('fin-measurement')
    }


@app.route('/proxy', methods=['POST'])
def proxy():
    payload = request.json
    rh_api_key = PayloadReqKey.apiKey.get_val(payload)
    if not rh_api_key == api_key:
        raise ConnectionAbortedError('API BYE')
    # client = _gen_request_client(payload)
    wd_path = os.path.dirname(__file__)
    spec = importlib.util.spec_from_file_location("action", f"{wd_path}/{PayloadReqKey.name.get_val(payload)}.py")
    foo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(foo)
    out_dict: dict = comm_utils.to_dict(foo.run(payload))
    return Response(json.dumps(out_dict), mimetype='application/json')


# def _gen_request_client(payload: dict) -> RequestClient:
#     return RequestClient(api_key=payload.get(PayloadReqKey.apiKey.value),
#                          secret_key=payload.get(PayloadReqKey.secret.value))


@contextmanager
def gen_ws_client(payload: dict) -> SubscriptionClient:
    sub_client = SubscriptionClient(api_key=payload.get(PayloadReqKey.apiKey.value),
                                    secret_key=payload.get(PayloadReqKey.secret.value))
    try:
        yield sub_client
    finally:
        sub_client.unsubscribe_all()


def get_flask_app():
    return app
