import exchange
from cron import cron_settings
from dto.account_dto import AccountDto
from infra import database
from rest.proxy_controller import PayloadReqKey
from service.wallet_client_service import WalletClientService
from utils import comm_utils
from utils.wallet_utils import WalletFilter


def run(payload: dict) -> AccountDto:
    PayloadReqKey.clean_default_keys(payload)
    if not payload:
        return get_current_payload()
    cron_settings.cancel_lend_by_filter_pyload = payload.get('cancel_lend_by_filter_pyload')
    cron_settings.lend_by_filter_payload = payload.get('lend_by_filter_payload')
    return get_current_payload()


def get_current_payload():
    return {
        'cancel_lend_by_filter_pyload': cron_settings.cancel_lend_by_filter_pyload,
        'lend_by_filter_payload': cron_settings.lend_by_filter_payload
    }
