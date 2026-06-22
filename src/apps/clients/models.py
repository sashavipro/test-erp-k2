import uuid
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.core.models.base import Base

class Client(Base):
    """
    SQLAlchemy model representing a Client in the ERP system.
    
    Attributes:
        id (UUID): The unique identifier for the client.
        name (str): The name of the client.
        email (str, optional): The email address of the client.
        orders (List[Order]): The list of orders associated with this client.
    """
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    email = Column(String, nullable=True)

    orders = relationship("Order", back_populates="client")
