import exchange
from infra.enums import PayloadReqKey
from service.market_client_sevice import MarketClientService
from utils import comm_utils


def run(payload: dict) -> dict:
    marketClient: MarketClientService = exchange.gen_impl_obj(
        exchange_name=PayloadReqKey.exchange.get_val(payload),
        clazz=MarketClientService, **payload)
    result = marketClient.get_exchange_info()
    return comm_utils.to_dict(result)
