from typing import List

from maicoin_max.client import Client
from maicoin_max.dto.wallet import Wallet

from dto.wallet_dto import WalletDto
from exchange.maicoin_max import gen_request_client, max_utils
from service.wallet_client_service import WalletClientService


class MaxWalletClientService(WalletClientService):

    def __init__(self, **kwargs):
        super(MaxWalletClientService, self).__init__(**kwargs)
        self.client: Client = gen_request_client()

    def list_all(self) -> List[WalletDto]:
        result: List[Wallet] = self.client.get_private_account_balances()
        return [max_utils.convert_wallet(w) for w in result]

    def cancel_lend_all(self, w: WalletDto):
        pass

    def lend_one(self, w: WalletDto, **kwargs) -> object:
        pass


def get_impl_clazz() -> MaxWalletClientService:
    return MaxWalletClientService
