from datetime import datetime

from sqlalchemy import Column, String, DECIMAL, Float, DateTime

from infra.database import Base
from model import TimestampMixin


class Order(Base, TimestampMixin):
    __tablename__ = 'order'
    uid = Column(String(12), primary_key=True)
    exchange = Column(String(50), nullable=False)
    exchangeOrderId = Column(String(255), nullable=True)
    batch_uid = Column(String(12), nullable=True)
    price = Column(Float, nullable=False)
    side = Column(String(50), nullable=False)
    status = Column(String(50), nullable=False)
    prd_name = Column(String(150), nullable=False)
    order_strategy = Column(String(50), nullable=False)
    exchange_update_at = Column(DateTime, default=datetime.utcnow)
    positionSide = Column(String(50), nullable=False)
