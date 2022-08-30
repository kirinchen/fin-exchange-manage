from typing import List, Dict

from dto.order_dto import OrderDto
from infra.enums import OrderType
from service import order_client_service
from utils import reflection_util


class OrderCreateDto:

    def __init__(self, **kwargs):
        self.prd_name: str = None
        self.ordertype: str = None
        self.positionSide: str = None
        self.quantity: float = -1.0
        self.marketed: bool = False
        self.price: float = -1.0
        self.tags: List[str] = list()
        reflection_util.merge(kwargs, self)


class OrderCreateBatchDto:

    def __init__(self, body: Dict[str, dict], **kwargs):
        reflection_util.merge(kwargs, self)
        self.body: Dict[str, OrderCreateDto] = dict()
        for key, value in body.items():
            self.body[key] = OrderCreateDto(**value)
