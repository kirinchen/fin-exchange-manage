from sqlalchemy import Column, String

from infra.database import Base


class Order(Base):
    __tablename__ = 'order'
    uid = Column(String(12), primary_key=True)
    exchange = Column(String(50), nullable=False)
    exchangeOrderId = Column(String(255), nullable=True)
