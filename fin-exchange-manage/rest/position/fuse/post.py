import exchange
from infra import database
from rest.position.fuse import DEFAULT_TAG
from rest.proxy_controller import PayloadReqKey
from service.position_fuse.mediation import StopMediation, StopMediationDto
from utils import comm_utils


def run(payload: dict) -> dict:
    with database.session_scope() as session:
        stopMediation: StopMediation = exchange.gen_impl_obj(exchange_name=PayloadReqKey.exchange.get_val(payload),
                                                             clazz=StopMediation, session=session)
        dto = StopMediationDto(**payload)
        dto.tags.append(DEFAULT_TAG)
        stopMediation.init(dto)
        return comm_utils.to_dict(stopMediation.stop())
