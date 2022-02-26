from typing import List

from maicoin_max.client import Client

from dto.wallet_dto import WalletDto
from exchange.maicoin_max import gen_request_client
from service.wallet_client_service import WalletClientService


class MaxWalletClientService(WalletClientService):

    def __init__(self, **kwargs):
        super(MaxWalletClientService, self).__init__(**kwargs)
        self.client: Client = gen_request_client()

    def list_all(self) -> List[WalletDto]:
        raise NotImplementedError("list_all")

    def cancel_lend_all(self, w: WalletDto):
        pass

    def lend_one(self, w: WalletDto, **kwargs) -> object:
        pass


def get_impl_clazz() -> MaxWalletClientService:
    return MaxWalletClientService
