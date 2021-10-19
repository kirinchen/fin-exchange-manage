from infra.database import Base
from sqlalchemy import Column, Integer, String, Float

from utils import comm_utils


class ExchangeProduct(Base):
    __tablename__ = 'exchange_product'
    uid = Column(String(12), primary_key=True, nullable=False)
    exchange = Column(String(50), nullable=False)
    item = Column(String(50), nullable=False)
    valuation_item = Column(String(50), nullable=False)
    precision_price = Column(Integer(12), nullable=False)
    precision_amount = Column(Integer(12), nullable=False)
    max_valuation_item = Column(Float(12), nullable=False)
    min_valuation_item = Column(Float(12), nullable=False)

    def __init__(self, exchange: str, item: str, valuation_item: str, precision_price: int, precision_amount: int,
                 max_valuation_item: float, min_valuation_item: float):
        self.exchange: str = exchange
        self.item: str = item
        self.valuation_item: str = valuation_item
        self.uid = comm_utils.to_sh256_str(f'{exchange}#{item}#{valuation_item}')
        self.precision_price: int = precision_price
        self.precision_amount: int = precision_amount
        self.max_valuation_item: float = max_valuation_item
        self.min_valuation_item: float = min_valuation_item
