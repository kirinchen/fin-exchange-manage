from abc import ABC

from service.base_exchange_abc import BaseExchangeAbc


class SyncCron(BaseExchangeAbc, ABC):

    def __init__(self, exchange_name: str):
        super(SyncCron, self).__init__(exchange_name)
