import config
from maicoin_max.client import Client


def gen_request_client() -> Client:
    key = config.env('maicoin-max-api-key')
    secret = config.env('maicoin-max-api-secret')
    return Client(key=key, secret=secret)
