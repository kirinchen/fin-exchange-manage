from typing import List

from dto.wallet_dto import WalletDto


class WalletFilter:

    def __init__(self, wallet_type: str = None, symbol: str = None, prd_name: str = None,
                 symbol_list: List[str] = list(),
                 **kwargs):
        self.wallet_type: str = wallet_type
        self.symbol: str = symbol
        self.symbol_list: List[str] = symbol_list
        self.prd_name: str = prd_name  # TODO impl


def filter_wallet(w_list: List[WalletDto], ft: WalletFilter) -> List[WalletDto]:
    ans: List[WalletDto] = list()
    for w in w_list:
        if ft.symbol and w.symbol != ft.symbol:
            continue
        if ft.wallet_type and w.wallet_type != ft.wallet_type:
            continue
        if len(ft.symbol_list) > 0 and w.symbol not in ft.symbol_list:
            continue
        ans.append(w)
    return ans
