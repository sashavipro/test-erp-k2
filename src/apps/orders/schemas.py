"""src/apps/orders/schemas.py."""

from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field


class OrderItemCreate(BaseModel):
    """Order item create schema."""

    product_id: UUID
    quantity: int = Field(default=1, ge=1)


class OrderCreate(BaseModel):
    """Order create schema."""

    client_id: UUID
    items: list[OrderItemCreate] = Field(..., min_length=1)


class OrderItemResponse(BaseModel):
    """Order item response schema."""

    id: UUID
    product_id: UUID
    quantity: int

    model_config = ConfigDict(from_attributes=True)


class OrderResponse(BaseModel):
    """Order response schema."""

    id: UUID
    client_id: UUID
    total_amount: Decimal
    created_at: datetime
    items: list[OrderItemResponse]

    model_config = ConfigDict(from_attributes=True)
