import abc
from abc import ABC
from typing import List

from dto.wallet_dto import WalletDto
from service.base_exchange_abc import BaseExchangeAbc


class WalletClientService(BaseExchangeAbc, ABC):

    def get_abc_clazz(self) -> object:
        return WalletClientService

    @abc.abstractmethod
    def list_all(self) -> List[WalletDto]:
        raise NotImplementedError('list_all')
