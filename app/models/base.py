from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, DateTime, Table, ForeignKey
from datetime import datetime

now = datetime.utcnow
Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=now, nullable=False)
    updated_at = Column(DateTime, default=now, onupdate=now, nullable=False)
