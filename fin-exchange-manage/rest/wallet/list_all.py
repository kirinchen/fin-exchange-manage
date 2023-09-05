import exchange
from dto.account_dto import AccountDto
from infra.enums import PayloadReqKey
from service.wallet_client_service import WalletClientService
from utils import comm_utils


def run(payload: dict) -> AccountDto:
    walletClient: WalletClientService = exchange.gen_impl_obj(
        exchange_name=PayloadReqKey.exchange.get_val(payload),
        clazz=WalletClientService, **payload)
    result = walletClient.list_all()
    return comm_utils.to_dict(result)
