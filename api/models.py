from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base

# Base class for SQLAlchemy models
Base = declarative_base()

class Product(Base):
    """
    SQLAlchemy model for Product entity.
    Represents a product managed by the platform.
    """
    __tablename__ = "products"

    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String(128), unique=True, nullable=False, index=True)
    description: str = Column(Text, nullable=True)
    created_at: datetime = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: datetime = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    created_by: str = Column(String(64), nullable=False)
    updated_by: str = Column(String(64), nullable=True)

    def __repr__(self) -> str:
        return f"<Product(id={self.id}, name='{self.name}')>"

# Exports
# - Base: SQLAlchemy declarative base
# - Product: Product model class