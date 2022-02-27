from typing import List

from dto.wallet_dto import WalletDto


class WalletFilter:

    def __init__(self, wallet_type: str = None, symbol: str = None, not_symbol: str = None, amount_exist: bool = None,
                 symbol_list: List[str] = list(),not_symbol_list: List[str] = list(),
                 **kwargs):
        self.wallet_type: str = wallet_type
        self.symbol: str = symbol
        self.not_symbol: str = not_symbol
        self.symbol_list: List[str] = symbol_list
        self.not_symbol_list: List[str] = not_symbol_list
        self.amount_exist: bool = amount_exist


def filter_wallet(w_list: List[WalletDto], ft: WalletFilter) -> List[WalletDto]:
    ans: List[WalletDto] = list()
    for w in w_list:
        if ft.symbol and w.symbol != ft.symbol:
            continue
        if ft.not_symbol and w.symbol == ft.not_symbol:
            continue
        if ft.wallet_type and w.wallet_type != ft.wallet_type:
            continue
        if len(ft.symbol_list) > 0 and w.symbol not in ft.symbol_list:
            continue
        if len(ft.not_symbol_list) > 0 and w.symbol in ft.not_symbol_list:
            continue
        if ft.amount_exist is not None:
            if ft.amount_exist and w.balance <= 0:
                continue
            if not ft.amount_exist and w.balance > 0:
                continue
        ans.append(w)
    return ans
