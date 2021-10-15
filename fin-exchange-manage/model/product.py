from infra.database import Base
from sqlalchemy import Column, Integer, String


class Product(Base):
    __tablename__ = 'product'
    name = Column(String(50), primary_key=True, nullable=False)
    symbol = Column(String(50), unique=True, nullable=False)

    def __init__(self, name: str, symbol: str):
        self.name = name
        self.symbol = symbol
