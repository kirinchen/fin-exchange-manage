from datetime import datetime

from sqlalchemy import Column, DateTime


class TimestampMixin(object):
    """Mixin class from system columns"""
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)