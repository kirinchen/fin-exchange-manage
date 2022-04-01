import json
from typing import List

from infra.database import Base
from sqlalchemy import Column, Integer, String


class Exchange(Base):
    __tablename__ = 'exchange'
    name = Column(String(50), primary_key=True, nullable=False)
    allowSides = Column(String(255))

    def __init__(self, name: str, sides: List[str]):
        self.name: str = name
        self.set_allow_sides(sides)

    def set_allow_sides(self, sides: List[str]):
        txt = json.dumps(sides)
        self.allowSides = txt

    def get_allow_sides(self) -> List[str]:
        return json.loads(self.allowSides)

    def get_dict(self) -> dict:
        return {
            'allowSides': self.get_allow_sides(),
            'name': self.name
        }
