class AccountDto:

    def __init__(self, maxWithdrawAmount: float, totalWalletBalance: float, **kwargs):
        self.maxWithdrawAmount = maxWithdrawAmount
        self.totalWalletBalance = totalWalletBalance
