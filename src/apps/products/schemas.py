"""src/apps/products/schemas.py."""

from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel
from pydantic import ConfigDict


class ProductBase(BaseModel):
    """Product base schema."""

    name: str
    price: Decimal


class ProductCreate(ProductBase):
    """Product create schema."""


class ProductResponse(ProductBase):
    """Product response schema."""

    id: UUID

    model_config = ConfigDict(from_attributes=True)
