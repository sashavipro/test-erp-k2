from pydantic import BaseModel, ConfigDict, Field
from uuid import UUID
from datetime import datetime
from typing import List
from decimal import Decimal

class OrderItemCreate(BaseModel):
    product_id: UUID
    quantity: int = Field(default=1, ge=1)

class OrderCreate(BaseModel):
    client_id: UUID
    items: List[OrderItemCreate] = Field(..., min_length=1)

class OrderItemResponse(BaseModel):
    id: UUID
    product_id: UUID
    quantity: int

    model_config = ConfigDict(from_attributes=True)

class OrderResponse(BaseModel):
    id: UUID
    client_id: UUID
    total_amount: Decimal
    created_at: datetime
    items: List[OrderItemResponse]

    model_config = ConfigDict(from_attributes=True)
