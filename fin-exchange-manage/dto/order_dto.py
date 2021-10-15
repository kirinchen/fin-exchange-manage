class OrderDto:

    def __init__(self,
                 clientOrderId=""
                 , cumQuote=0.0
                 , executedQty=None
                 , orderId=None
                 , origQty=None
                 , price=None
                 , side=None
                 , status=None
                 , stopPrice=None
                 , symbol=""
                 , type=None
                 , updateTime=0
                 , avgPrice=0.0
                 , origType=""
                 , positionSide=""
                 , activatePrice=None
                 , priceRate=None
                 , closePosition=None
                 , **kwargs
                 ):
        self.clientOrderId = clientOrderId
        self.cumQuote = cumQuote
        self.executedQty = executedQty
        self.orderId = orderId
        self.origQty = origQty
        self.price = price
        self.side = side
        self.status = status
        self.stopPrice = stopPrice
        self.symbol = symbol
        self.type = type
        self.updateTime = updateTime
        self.avgPrice = avgPrice
        self.origType = origType
        self.positionSide = positionSide
        self.activatePrice = activatePrice
        self.priceRate = priceRate
        self.closePosition = closePosition
