from infra.database import Base
from sqlalchemy import Column, Integer, String


class Exchange(Base):
    __tablename__ = 'exchange'
    name = Column(String(50), primary_key=True, nullable=False)

    def __init__(self, name: str):
        self.name: str = name
