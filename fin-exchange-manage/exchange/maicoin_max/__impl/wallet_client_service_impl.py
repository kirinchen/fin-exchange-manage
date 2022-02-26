from typing import List

from maicoin_max.client import Client

from exchange.maicoin_max import gen_request_client


class MaxWalletClientService(WalletClientService):

    def __init__(self, **kwargs):
        super(MaxWalletClientService, self).__init__(**kwargs)
        self.client: Client = gen_request_client()

    def list_all(self) -> List[WalletDto]:
        u_w: AccountDto = account.info.get.invoke(self.exchange_name)
        ans = WalletDto()
        ans.wallet_type = 'U'
        ans.symbol = 'USDT'
        ans.uid = 'U_USDT'
        ans.balance = u_w.totalWalletBalance
        ans.balance_available = u_w.maxWithdrawAmount
        return [ans]

    def cancel_lend_all(self, w: WalletDto):
        pass

    def lend_one(self, w: WalletDto, **kwargs) -> object:
        pass


def get_impl_clazz() -> MaxWalletClientService:
    return MaxWalletClientService
