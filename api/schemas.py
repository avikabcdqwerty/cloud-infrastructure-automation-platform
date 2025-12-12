from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, constr

class ProductBase(BaseModel):
    """
    Shared properties for Product.
    """
    name: constr(strip_whitespace=True, min_length=1, max_length=128) = Field(..., example="Cloud Automation Suite")
    description: Optional[str] = Field(None, example="A platform for automating cloud infrastructure.")

class ProductCreate(ProductBase):
    """
    Properties required to create a Product.
    """
    pass

class ProductUpdate(BaseModel):
    """
    Properties allowed for updating a Product.
    """
    name: Optional[constr(strip_whitespace=True, min_length=1, max_length=128)] = Field(None, example="Cloud Automation Suite")
    description: Optional[str] = Field(None, example="Updated description for the product.")

class Product(ProductBase):
    """
    Product response schema.
    """
    id: int = Field(..., example=1)
    created_at: datetime = Field(..., example="2024-06-01T12:00:00Z")
    updated_at: datetime = Field(..., example="2024-06-01T12:30:00Z")
    created_by: str = Field(..., example="admin")
    updated_by: Optional[str] = Field(None, example="admin")

    class Config:
        orm_mode = True

# Exports:
# - ProductBase: shared product properties
# - ProductCreate: schema for product creation
# - ProductUpdate: schema for product update
# - Product: schema for product response