from apscheduler.schedulers.background import BackgroundScheduler

from cron.bzk_flow_off_restart import BzkFlowOffRestart
from cron.lend_funding_job import LendFundingJob

scheduler = BackgroundScheduler()

lend_funding_job_tom = LendFundingJob('-tom')
lend_funding_job = LendFundingJob()

bzk_flow_off_restart = BzkFlowOffRestart()


def start_all():
    scheduler.add_job(func=bzk_flow_off_restart.check_and_restart, trigger="interval", seconds=2 * 60)
    scheduler.add_job(func=lend_funding_job.lend, trigger="interval", seconds=25 * 60)
    scheduler.add_job(func=lend_funding_job_tom.lend, trigger="interval", seconds=37 * 60)
    scheduler.start()
