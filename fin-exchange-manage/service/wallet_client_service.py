import abc
from abc import ABC
from typing import List

from dto.wallet_dto import WalletDto
from service.base_exchange_abc import BaseExchangeAbc
from utils import wallet_utils
from utils.wallet_utils import WalletFilter


class WalletClientService(BaseExchangeAbc, ABC):

    def get_abc_clazz(self) -> object:
        return WalletClientService

    @abc.abstractmethod
    def list_all(self) -> List[WalletDto]:
        raise NotImplementedError('list_all')

    def query(self, ft: WalletFilter) -> List[WalletDto]:
        return wallet_utils.filter_wallet(self.list_all(), ft)

    def get_one(self, ft: WalletFilter) -> WalletDto:
        return self.query(ft)[0]

    def lend_by_filter(self, ft: WalletFilter, **kwargs) -> List[object]:
        w_list = self.query(ft)
        ans: List[object] = list()
        for w in w_list:
            ans.append(self.lend_one(w, **kwargs))
        return ans

    def cancel_lend_by_filter(self, ft: WalletFilter, **kwargs) -> List[object]:
        w_list = self.query(ft)
        ans: List[object] = list()
        for w in w_list:
            ans.append(self.cancel_lend_all(w))
        return ans

    @abc.abstractmethod
    def cancel_lend_all(self, w: WalletDto):
        raise NotImplementedError('cancel_lend_all')

    @abc.abstractmethod
    def lend_one(self, w: WalletDto, **kwargs) -> object:
        raise NotImplementedError('list_all')
