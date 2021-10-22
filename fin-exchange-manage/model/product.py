from infra.database import Base
from sqlalchemy import Column, Integer, String, Float

from utils import comm_utils


class Product(Base):
    __tablename__ = 'product'
    uid = Column(String(32), primary_key=True, nullable=False)
    exchange = Column(String(50), nullable=False)
    item = Column(String(50), nullable=False)
    valuation_item = Column(String(50), nullable=False)
    precision_price = Column(Integer, nullable=True)
    precision_amount = Column(Integer, nullable=True)
    max_item = Column(Float, nullable=True)
    min_item = Column(Float, nullable=True)
    max_valuation_item = Column(Float, nullable=True)
    min_valuation_item = Column(Float, nullable=True)

    def __init__(self, exchange: str, item: str, valuation_item: str, precision_price: int = None,
                 precision_amount: int = None,
                 max_valuation_item: float = None, min_valuation_item: float = None, max_item: float = None,
                 min_item: float = None):
        self.exchange: str = exchange
        self.item: str = item
        self.valuation_item: str = valuation_item
        self.uid = get_uid(exchange, item, valuation_item)[:32]
        self.precision_price: int = precision_price
        self.precision_amount: int = precision_amount
        self.max_valuation_item: float = max_valuation_item
        self.min_valuation_item: float = min_valuation_item
        self.max_item: float = max_item
        self.min_item: float = min_item


def get_uid(exchange: str, item: str, valuation_item: str) -> str:
    return comm_utils.to_sh256_str(f'{exchange}#{item}#{valuation_item}')[:32]
