import config
from binance_f import RequestClient


def gen_request_client() -> RequestClient:
    return RequestClient(api_key=config.env('binance-api-key'),
                         secret_key=config.env('binance-api-secret'))
