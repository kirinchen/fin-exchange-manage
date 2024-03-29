import contextvars
import importlib.util
import json
import os
from contextlib import contextmanager
from datetime import datetime

from binance_f import SubscriptionClient
from flask import Flask, Response
from flask import request

import config
from cron import bzk_flow_off_restart_job
from infra.enums import PayloadReqKey
from utils import comm_utils

api_key = config.env('api-key')

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


exchange_account_context = contextvars.ContextVar(PayloadReqKey.exchange_account.value, default=None)


@app.route('/proxy', methods=['POST'])
def proxy():
    payload = request.json
    rh_api_key = PayloadReqKey.apiKey.get_val(payload)
    if not rh_api_key == api_key:
        raise ConnectionAbortedError('API BYE')
    bzk_flow_off_restart_job.notify_new_request(payload)
    PayloadReqKey.clean_sensitive_keys(payload)
    exchange_account_context.set(payload.get(PayloadReqKey.exchange_account.value, None))
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
