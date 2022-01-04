from utils import reflection_util


class WalletDto:

    def __init__(self, **kwargs):
        self.wallet_type: str = None
        self.symbol: str = None
        self.balance: float = None
        self.balance_available: float = None
        self.uid: str = None
        reflection_util.merge(kwargs, self)
