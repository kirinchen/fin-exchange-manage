import exchange
from dto.account_dto import AccountDto
from infra.enums import PayloadReqKey
from service.wallet_client_service import WalletClientService
from utils import comm_utils
from utils.wallet_utils import WalletFilter


def run(payload: dict) -> AccountDto:
    w_filter: WalletFilter = WalletFilter(**payload)
    walletClient: WalletClientService = exchange.gen_impl_obj(
        exchange_name=PayloadReqKey.exchange.get_val(payload),
        clazz=WalletClientService, **payload)
    result = walletClient.cancel_lend_by_filter(w_filter, **payload)
    return comm_utils.to_dict(result)
