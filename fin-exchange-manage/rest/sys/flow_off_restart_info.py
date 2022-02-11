import exchange
from cron import cron_settings
from dto.account_dto import AccountDto
from infra import database
from infra.enums import PayloadReqKey
from service.wallet_client_service import WalletClientService
from utils import comm_utils


def run(payload: dict) -> AccountDto:
    result: dict = cron_settings.bzk_flow_off_restart.get_info()
    return comm_utils.to_dict(result)
