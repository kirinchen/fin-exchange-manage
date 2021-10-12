from infra.database import Base
from sqlalchemy import Column, Integer, String


class ExchangeProduct(Base):
    __tablename__ = 'exchange_product'
    uid = Column(String(12), primary_key=True, nullable=False)
    exchange = Column(String(50), nullable=False)
    product = Column(String(50), nullable=False)
