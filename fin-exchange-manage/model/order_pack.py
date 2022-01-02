import json
from typing import List

from sqlalchemy import Column, String, Text, Float

from infra.database import Base
from model.comm import TimestampMixin


class OrderPack(Base, TimestampMixin):
    __tablename__ = 'order_pack'
    uid = Column(String(12), primary_key=True)
    exchange = Column(String(50), nullable=False)
    order_strategy = Column(String(50), nullable=False)
    tags = Column(Text, nullable=True)
    attach = Column(Text, nullable=True)
    attach_name = Column(String(255), nullable=True)
    parameters = Column(Text, nullable=True)
    market_price = Column(Float, nullable=False)
    side = Column(String(50), nullable=False)
    prd_name = Column(String(150), nullable=False)
    positionSide = Column(String(50), nullable=False)

    def set_tags(self, tags: List[str]):
        if tags is None:
            return
        self.tags = json.dumps(tags)

    def get_tags(self) -> List[str]:
        return json.loads(self.tags)

    def set_attach(self, obj: dict):
        if obj is None:
            return
        self.attach = json.dumps(obj)

    def get_attach(self) -> dict:
        return json.loads(self.attach)

    def set_parameters(self, parameters: dict):
        if parameters is None:
            return
        self.parameters = json.dumps(parameters)

    def get_parameters(self) -> dict:
        return json.loads(self.parameters)
