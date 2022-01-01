import json
from datetime import datetime
from typing import List

from sqlalchemy import Column, String, DECIMAL, Float, DateTime, Text

from infra.database import Base
from model.comm import TimestampMixin


class Order(Base, TimestampMixin):
    __tablename__ = 'order'
    uid = Column(String(12), primary_key=True)
    exchange = Column(String(50), nullable=False)
    exchangeOrderId = Column(String(255), nullable=True)
    pack_uid = Column(String(12), nullable=True)
    price = Column(Float, nullable=False)
    side = Column(String(50), nullable=False)
    status = Column(String(50), nullable=False)
    prd_name = Column(String(150), nullable=False)
    order_strategy = Column(String(50), nullable=True)
    exchange_update_at = Column(DateTime, default=datetime.utcnow)
    positionSide = Column(String(50), nullable=False)
    tags = Column(Text, nullable=True)

    def set_tags(self, tags: List[str]):
        self.tags = json.dumps(tags)

    def get_tags(self) -> List[str]:
        return json.loads(self.tags)
