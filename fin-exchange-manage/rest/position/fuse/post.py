import exchange
from infra import database
from rest.position.fuse import DEFAULT_TAG
from infra.enums import PayloadReqKey
from service.position_fuse.mediation import StopMediation, StopMediationDto
from utils import comm_utils


def run(payload: dict) -> dict:
    try:
        with database.session_scope() as session:
            stopMediation: StopMediation = exchange.gen_impl_obj(exchange_name=PayloadReqKey.exchange.get_val(payload),
                                                                 clazz=StopMediation, session=session, **payload)
            dto = StopMediationDto(**payload)
            dto.tags.append(DEFAULT_TAG)
            stopMediation.init(dto)
            return comm_utils.to_dict(stopMediation.stop())
    except Exception as e:  # work on python 3.x
        return {
            'type': str(type(e)),
            'msg': str(e)
        }
