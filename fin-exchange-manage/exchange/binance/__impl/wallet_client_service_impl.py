from typing import List

from binance_f import RequestClient
from sqlalchemy.orm import Session

from dto.account_dto import AccountDto
from dto.wallet_dto import WalletDto
from exchange.binance import gen_request_client
from rest import account
from service.wallet_client_service import WalletClientService


class BinanceWalletClientService(WalletClientService):

    def __init__(self, exchange_name: str, session: Session = None):
        super(BinanceWalletClientService, self).__init__(exchange_name, session)
        self.client: RequestClient = gen_request_client()

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


def get_impl_clazz() -> BinanceWalletClientService:
    return BinanceWalletClientService
