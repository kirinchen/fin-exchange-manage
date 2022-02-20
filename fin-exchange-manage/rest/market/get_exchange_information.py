import exchange
from infra import database
from infra.enums import PayloadReqKey
from service.market_client_sevice import MarketClientService
from utils import comm_utils


def run(payload: dict) -> dict:
    with database.session_scope() as session:
        marketClient: MarketClientService = exchange.gen_impl_obj(
            exchange_name=PayloadReqKey.exchange.get_val(payload),
            clazz=MarketClientService, session=session, **payload)
        result = marketClient.get_exchange_info()
        return comm_utils.to_dict(result)
