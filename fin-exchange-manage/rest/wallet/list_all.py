import exchange
from dto.account_dto import AccountDto
from infra import database
from infra.enums import PayloadReqKey
from service.wallet_client_service import WalletClientService
from utils import comm_utils


def run(payload: dict) -> AccountDto:
    with database.session_scope() as session:
        walletClient: WalletClientService = exchange.gen_impl_obj(
            exchange_name=PayloadReqKey.exchange.get_val(payload),
            clazz=WalletClientService, session=session,**payload)
        result = walletClient.list_all()
        return comm_utils.to_dict(result)
