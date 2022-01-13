from typing import List


class BaseFuseDto:

    def __init__(self, prd_name: str, positionSide: str, fuseStrategy: str, **kwargs):
        self.prd_name: str = prd_name
        self.positionSide: str = positionSide
        self.fuseStrategy: str = fuseStrategy


class FixedStepFuseDto(BaseFuseDto):

    def __init__(self, minCount: int, priceStep: float, rebuildByPriceStepRate: float, noLoseBaseCount: int,
                 proportionalRate: float,
                 tags: List[str] = list(), **kwargs):
        super().__init__(**kwargs)
        self.tags: List[str] = tags
        self.minCount: int = minCount
        self.priceStep: float = priceStep
        self.rebuildByPriceStepRate: float = rebuildByPriceStepRate
        self.noLoseBaseCount: int = noLoseBaseCount
        self.proportionalRate: float = proportionalRate
