class Trade:

    def __init__(self, price:float, qty:float, quoteQty:float):

        self.price :float=price
        self.qty:float = qty
        self.quoteQty:float = quoteQty
        self.time: = 0
        self.isBuyerMaker = False