import uuid
from sqlalchemy import Column, String, Numeric
from sqlalchemy.dialects.postgresql import UUID

from src.core.models.base import Base

class Product(Base):
    """
    SQLAlchemy model representing a Product in the ERP system.
    
    Attributes:
        id (UUID): The unique identifier for the product.
        name (str): The name of the product.
        price (Decimal): The price of the product.
    """
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
