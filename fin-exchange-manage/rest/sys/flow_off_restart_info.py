from cron import bzk_flow_off_restart_job
from dto.account_dto import AccountDto
from utils import comm_utils


def run(payload: dict) -> AccountDto:
    result: dict = bzk_flow_off_restart_job.instance.get_info()
    return comm_utils.to_dict(result)
