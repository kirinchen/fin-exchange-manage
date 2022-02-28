from cron import cron_settings
from cron.lend_funding_job import LendFundingJob
from dto.account_dto import AccountDto
from infra.enums import PayloadExKey, PayloadReqKey
from utils import comm_utils


def run(payload: dict) -> AccountDto:
    PayloadReqKey.clean_default_keys(payload)
    if not payload.get('cancel_lend_by_filter_pyload', None) and not payload.get('lend_by_filter_payload', None):
        return get_current_info(payload)
    update_job_payload(payload)
    return get_current_info(payload)


def _get_job(payload: dict) -> LendFundingJob:
    account: str = PayloadExKey.exchange_account.get_val(payload, None)
    return cron_settings.lend_funding_job_tom if account else cron_settings.lend_funding_job


def update_job_payload(payload: dict):
    job = _get_job(payload)
    job.cancel_lend_by_filter_pyload = payload.get('cancel_lend_by_filter_pyload')
    job.lend_by_filter_usd_payload = payload.get('lend_by_filter_payload')


def get_current_info(payload: dict):
    job = _get_job(payload)
    return comm_utils.to_dict(job.get_lend_info())
