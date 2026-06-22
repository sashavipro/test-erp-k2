from pydantic import BaseModel, ConfigDict
from uuid import UUID
from decimal import Decimal

class ProductBase(BaseModel):
    name: str
    price: Decimal

class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: UUID

    model_config = ConfigDict(from_attributes=True)
