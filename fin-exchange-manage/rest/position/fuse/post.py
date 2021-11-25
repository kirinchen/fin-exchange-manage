import exchange
from infra import database
from rest.proxy_controller import PayloadReqKey
from service.position_fuse.mediation import StopMediation, StopMediationDto
from utils import comm_utils


def run(payload: dict) -> dict:
    with database.session_scope() as session:
        stopMediation: StopMediation = exchange.gen_impl_obj(exchange_name=PayloadReqKey.exchange.get_val(payload),
                                                             clazz=StopMediation, session=session)
        dto = StopMediationDto(**payload)
        stopMediation.init(dto)
        return comm_utils.to_dict(stopMediation.stop())
