from datetime import datetime

from sqlalchemy import Column, DateTime

from .exchange import Exchange
from .item import Item
from .order import Order
from .product import Product
from .warehouse import Warehouse


class TimestampMixin(object):
    """Mixin class from system columns"""
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
