from sqlalchemy import Column, String

from infra.database import Base


class Warehouse(Base):
    __tablename__ = 'warehouse'
    uid = Column(String(12), primary_key=True)
    exchange = Column(String(50),  nullable=False)


