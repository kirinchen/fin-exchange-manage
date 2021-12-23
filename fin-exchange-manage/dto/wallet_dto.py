class WalletDto:

    def __init__(self, uid: str, symbol: str, balance: float, balance_available: float, clazz: str, **kwargs):
        self.clazz: str = clazz
        self.symbol: str = symbol
        self.balance: float = balance
        self.balance_available: float = balance_available
        self.uid: str = uid
