import exchange
from dto.account_dto import AccountDto
from dto.position_dto import PositionFilter
from infra.enums import PayloadReqKey
from service.position_client_service import PositionClientService
from utils import comm_utils


def run(payload: dict) -> AccountDto:
    pf = PositionFilter(**payload)
    positionClient: PositionClientService = exchange.gen_impl_obj(
        exchange_name=PayloadReqKey.exchange.get_val(payload),
        clazz=PositionClientService, **payload)
    result = positionClient.query(pf)
    return comm_utils.to_dict(result)
