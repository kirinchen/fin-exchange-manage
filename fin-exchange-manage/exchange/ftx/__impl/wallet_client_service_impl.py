from typing import List

from bfxapi import Wallet

from dto.wallet_dto import WalletDto
from exchange.ftx import gen_client

from infra.enums import PayloadExKey
from service.wallet_client_service import WalletClientService

LEND_MIN_AMOUNT = 50


class FTXWalletClientService(WalletClientService):

    def __init__(self, **kwargs):
        super(FTXWalletClientService, self).__init__(**kwargs)
        self.client = gen_client()

    def list_all(self) -> List[WalletDto]:
        return [WalletDto(symbol='USDT'), WalletDto(symbol='USD')]  # TODO impl Wallet list_all

    def cancel_lend_all(self, w: WalletDto):
        pass

    def lend_one(self, w: WalletDto, **kwargs) -> object:
        balance = self.client.get_private_wallet_single_balance(w.symbol)['total']
        r = self._get_rate_by_wallet(w) * 0.7
        return self.client.set_private_margin_lending_offer(w.symbol, balance, r)

    def _get_rate_by_wallet(self, w: WalletDto) -> float:
        rate = self.client.get_private_margin_lending_rates()
        for i in range(len(rate)):
            if rate[i]['coin'] == w.symbol:
                return rate[i]['estimate']
        raise NotImplementedError(f'_get_rate_by_wallet {w.symbol}')


def get_impl_clazz() -> FTXWalletClientService:
    return FTXWalletClientService
