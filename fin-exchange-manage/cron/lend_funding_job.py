import traceback
from datetime import datetime

from infra.enums import PayloadExKey
from rest.wallet import cancel_lend_by_filter, lend_by_filter

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
lend_by_filter_usd_payload = {
    "__bzk_api_key": '',
    "name": "wallet/lend_by_filter",
    "symbol": "USD",
    "rowAmount": 152,
    "minMaxDiffRate": 1.8,
    "middleWeight": 0.926,
    "wallet_type": "funding",
    "exchange": "bitfinex"
}

lend_by_filter_usdt_payload = {
    "__bzk_api_key": '',
    "name": "wallet/lend_by_filter",
    "symbol": "UST",
    "rowAmount": 160,
    "minMaxDiffRate": 0.286,
    "middleWeight": 0.4,
    "wallet_type": "funding",
    "exchange": "bitfinex"
}


class LendFundingJob:

    def __init__(self, mege_cfg: dict = {}):
        self.cancel_lend_by_filter_pyload = dict(cancel_lend_by_filter_pyload)
        self.lend_by_filter_usd_payload = dict(lend_by_filter_usd_payload)
        self.lend_by_filter_usdt_payload = dict(lend_by_filter_usdt_payload)
        self.cancel_lend_by_filter_pyload.update(mege_cfg)
        self.lend_by_filter_usd_payload.update(mege_cfg)
        self.lend_by_filter_usdt_payload.update(mege_cfg)
        self.lendCount = 0
        self.lastAt = datetime.now()
        self.lastException: dict = None

    def lend(self):
        try:
            print('lend_funding start')
            self.lastAt = datetime.now()
            self.lendCount += 1
            cancel_lend_by_filter.run(self.cancel_lend_by_filter_pyload)
            lend_by_filter.run(self.lend_by_filter_usd_payload)
            lend_by_filter.run(self.lend_by_filter_usdt_payload)
            print('lend_funding end')
        except Exception as e:  # work on python 3.x
            self.lastException = {
                '__error_type': str(type(e)),
                'msg': str(e),
                'traceback': traceback.format_exc()
            }

    def get_lend_info(self) -> dict:
        return self.__dict__
