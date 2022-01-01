from sqlalchemy import Column, String, Text

from infra.database import Base
from model import TimestampMixin


class OrderBatch(Base, TimestampMixin):
    __tablename__ = 'order_batch'
    uid = Column(String(12), primary_key=True)
    exchange = Column(String(50), nullable=False)
    order_strategy = Column(String(50), nullable=False)
    tags = Column(String(Text), nullable=True)
    attach = Column(String(Text), nullable=True)
