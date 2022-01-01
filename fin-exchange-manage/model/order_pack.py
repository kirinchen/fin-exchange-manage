import json
from typing import List

from sqlalchemy import Column, String, Text

from infra.database import Base
from model.comm import TimestampMixin


class OrderPack(Base, TimestampMixin):
    __tablename__ = 'order_pack'
    uid = Column(String(12), primary_key=True)
    exchange = Column(String(50), nullable=False)
    order_strategy = Column(String(50), nullable=False)
    tags = Column(Text, nullable=True)
    attach = Column(Text, nullable=True)

    def set_tags(self, tags: List[str]):
        self.tags = json.dumps(tags)

    def get_tags(self) -> List[str]:
        return json.loads(self.tags)

    def set_attach(self, obj: dict):
        self.attach = json.dumps(obj)

    def get_attach(self) -> dict:
        return json.loads(self.attach)
