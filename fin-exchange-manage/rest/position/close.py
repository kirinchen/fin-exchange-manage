import exchange
from infra.enums import PayloadReqKey
from service.position_client_service import PositionClientService
from utils import comm_utils


def run(payload: dict) -> dict:
    positionClient: PositionClientService = exchange.gen_impl_obj(
        exchange_name=PayloadReqKey.exchange.get_val(payload),
        clazz=PositionClientService, **payload)
    resp = positionClient.close(payload.get('prd_name'), payload.get('positionSide'), payload.get('amount'))
    return comm_utils.to_dict(resp)
