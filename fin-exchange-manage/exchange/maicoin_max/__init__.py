import config
from max_exchange_api_python3.max.client import Client


def gen_request_client() -> Client:
    return Client(config.env('maicoin-max-api-key'), config.env('maicoin-max-api-secret'))
