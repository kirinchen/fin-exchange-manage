import exchange
from infra import database
from infra.enums import PayloadReqKey
from service.trade_client_service import TradeClientService
from utils import comm_utils


def run(payload: dict) -> dict:
    with database.session_scope() as session:
        sbl: str = payload.get('symbol')
        limit = payload.get('limit')
        timeMaped: bool = payload.get('timeMaped', False)
        tradeClient: TradeClientService = exchange.gen_impl_obj(
            exchange_name=PayloadReqKey.exchange.get_val(payload),
            clazz=TradeClientService, session=session,**payload)
        result = tradeClient.fetch_recent_set(symbol=sbl, limit=limit, time_maped=timeMaped)
        return comm_utils.to_dict(result)
