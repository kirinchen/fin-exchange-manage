class BaseFuseDto:

    def __init__(self, prd_name: str, positionSide: str, **kwargs):
        self.prd_name: str = prd_name
        self.positionSide: str = positionSide


class FixedStepFuseDto(BaseFuseDto):

    def __init__(self, minCount: int, priceStep: float, **kwargs):
        super().__init__(**kwargs)
        self.minCount: int = minCount
        self.priceStep: float = priceStep
