import traceback

import exchange
from infra import database
from infra.enums import PayloadReqKey
from service.wallet_client_service import WalletClientService
from utils import comm_utils
from utils.wallet_utils import WalletFilter


def run(payload: dict) -> dict:
    try:
        with database.session_scope() as session:
            w_filter: WalletFilter = WalletFilter(**payload)
            walletClient: WalletClientService = exchange.gen_impl_obj(
                exchange_name=PayloadReqKey.exchange.get_val(payload),
                clazz=WalletClientService, session=session,**payload)
            result = walletClient.lend_by_filter(w_filter, **payload)
            return comm_utils.to_dict(result)
    except Exception as e:  # work on python 3.x
        return {
            '__error_type': str(type(e)),
            'msg': str(e),
            'traceback': traceback.format_exc()
        }
