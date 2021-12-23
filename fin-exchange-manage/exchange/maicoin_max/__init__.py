import config
from max_exchange_api_python3.maicoin_max.client import Client


def gen_request_client() -> Client:
    return Client(config.env('maicoin-maicoin_max-api-key'), config.env('maicoin-maicoin_max-api-secret'))
