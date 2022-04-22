import config

from exchange.ftx.client.client import Client

INPUT_YOUR_API_KEY1 = config.env('ftx-api-key')
INPUT_YOUR_API_SECRET1 = config.env('ftx-api-secret')
INPUT_YOUR_SUBACCOUNT_NAME1 = config.env('ftx-api-subaccount')


def gen_client() -> Client:
    return Client(INPUT_YOUR_API_KEY1, INPUT_YOUR_API_SECRET1,
                  INPUT_YOUR_SUBACCOUNT_NAME1)
