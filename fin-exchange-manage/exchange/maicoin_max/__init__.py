import config
from maicoin_max.client import Client


def gen_request_client() -> Client:
    return Client(config.env('maicoin-maicoin_max-api-key'), config.env('maicoin-maicoin_max-api-secret'))
