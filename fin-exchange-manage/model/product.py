from infra.database import Base
from sqlalchemy import Column, Integer, String


class Product(Base):
    __tablename__ = 'product'
    pid = Column(Integer, primary_key=True)
    name = Column(String(30), unique=True, nullable=False)
    price = Column(Integer, nullable=False)
    img = Column(String(100), unique=True, nullable=False)
    description = Column(String(255), nullable=False)
    state = Column(String(10), nullable=False)

    def __init__(self, name, price, img, description, state):
        self.name = name
        self.price = price
        self.img = img
        self.description = description
        self.state = state
