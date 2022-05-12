from apscheduler.schedulers.background import BackgroundScheduler

import config
from cron import bzk_flow_off_restart_job
from cron.lend_funding_job import LendFundingJob
from infra.enums import PayloadExKey

lend_funding_job_tom = LendFundingJob({PayloadExKey.exchange_account.value: '-tom'})
lend_funding_job = LendFundingJob()
lend_funding_job_ftx = LendFundingJob({
    "symbol_list": [
        "USDT", "USD"
    ],
    "wallet_type": None,
    "symbol": None,
    "exchange": "ftx"
})


def start_all():
    cron_enable = config.env_bool('cron_enable')
    if not cron_enable:
        return
    print(__file__ + ' start_all')
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=bzk_flow_off_restart_job.check, trigger="interval", seconds=2 * 60)
    #scheduler.add_job(func=lend_funding_job.lend, trigger="interval", seconds=25 * 60)
    scheduler.add_job(func=lend_funding_job_tom.lend, trigger="interval", seconds=25 * 60)
    #scheduler.add_job(func=lend_funding_job_ftx.lend, trigger="interval", seconds=1.01 * 60 * 60)
    scheduler.start()
