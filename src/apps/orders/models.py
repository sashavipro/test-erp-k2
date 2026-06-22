"""src/apps/orders/models.py."""

import uuid
from datetime import datetime

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.core.models.base import Base


class Order(Base):
    """SQLAlchemy model representing an Order placed by a Client.

    Attributes:
        id (UUID): The unique identifier for the order.
        client_id (UUID): The foreign key linking to the associated client.
        total_amount (Decimal): The automatically calculated total price of the order.
        created_at (datetime): The timestamp when the order was created.
        client (Client): The client who placed the order.
        items (List[OrderItem]): The items included in the order.

    """

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    client_id = Column(UUID(as_uuid=True), ForeignKey("clients.id"), nullable=False)
    total_amount = Column(Numeric(10, 2), nullable=False, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    client = relationship("Client", back_populates="orders")
    items = relationship("OrderItem", back_populates="order")


class OrderItem(Base):
    """SQLAlchemy model representing a specific item (product) within an Order.

    Attributes:
        id (UUID): The unique identifier for the order item.
        order_id (UUID): The foreign key linking to the parent order.
        product_id (UUID): The foreign key linking to the associated product.
        quantity (int): The number of units of the product ordered.
        order (Order): The parent order.
        product (Product): The associated product.

    """

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.id"), nullable=False)
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)

    order = relationship("Order", back_populates="items")
    product = relationship("Product")
