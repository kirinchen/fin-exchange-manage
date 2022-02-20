import json

from infra.database import Base
from sqlalchemy import Column, Integer, String, Float, Text

from utils import comm_utils


class Product(Base):
    __tablename__ = 'product'
    uid = Column(String(32), primary_key=True, nullable=False)
    exchange = Column(String(50), nullable=False)
    prd_name = Column(String(150), nullable=False)  # ex NSDAQUSD USDTWD ... but U本位幣安例外 BTC ETH ...
    item = Column(String(50), nullable=False)
    valuation_item = Column(String(50), nullable=False)
    config = Column(Text, nullable=False)

    def __init__(self, exchange: str, item: str, valuation_item: str, prd_name: str, config: dict = None):
        self.exchange: str = exchange
        self.item: str = item
        self.prd_name: str = prd_name
        self.valuation_item: str = valuation_item
        self.uid: str = get_uid(exchange, item, valuation_item)[:32]
        self.set_config(config)

    def set_config(self, cfg: dict):
        self.config = json.dumps(cfg)

    def get_config(self) -> dict:
        return json.loads(self.config)


def get_uid(exchange: str, item: str, valuation_item: str) -> str:
    return comm_utils.to_sh256_str(f'{exchange}#{item}#{valuation_item}')[:32]
