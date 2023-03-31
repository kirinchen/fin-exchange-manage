import config
from binance_f import RequestClient

from rest import proxy_controller


def gen_request_client() -> RequestClient:
    account_info = proxy_controller.exchange_account_context.get()
    api_url: str = 'https://fapi.binance.com' if account_info != 'dev' else 'https://testnet.binancefuture.com'
    key_prefix: str = f'binance-api-{account_info}' if account_info else 'binance-api'
    return RequestClient(api_key=config.env(key_prefix + '-key'),
                         secret_key=config.env(key_prefix + '-secret'),
                         url=api_url)
