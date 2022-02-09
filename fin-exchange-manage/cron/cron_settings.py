import time
import atexit

from apscheduler.schedulers.background import BackgroundScheduler

import config
from rest.wallet import lend_by_filter, cancel_lend_by_filter

scheduler = BackgroundScheduler()

funding_currency_list = [
    "USD",
    "UST"
]
cancel_lend_by_filter_pyload = {
    "__bzk_api_key": '',
    "name": "wallet/cancel_lend_by_filter",
    "symbol_list": funding_currency_list,
    "wallet_type": "funding",
    "exchange": "bitfinex"
}
lend_by_filter_payload = {
    "__bzk_api_key": '',
    "name": "wallet/lend_by_filter",
    "symbol_list": funding_currency_list,
    "rowAmount": 100,
    "bottomWeight": 1.01,
    "topWeight": 1.01,
    "middleWeight": 0.28,
    "wallet_type": "funding",
    "exchange": "bitfinex"
}


def lend_funding():
    cancel_lend_by_filter.run(cancel_lend_by_filter_pyload)
    time.sleep(10)
    lend_by_filter.run(lend_by_filter_payload)


def start_all():
    scheduler.add_job(func=lend_funding, trigger="interval", seconds=25*60)
    scheduler.start()
