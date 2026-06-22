"""src/apps/orders/repositories.py."""

from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from src.apps.clients.models import Client
from src.apps.orders.models import Order
from src.apps.orders.models import OrderItem
from src.apps.products.models import Product


class OrderRepository:
    """Order repository."""

    def __init__(self, session: AsyncSession):
        """Initialize repository."""
        self.session = session

    async def get_client_by_id(self, client_id: UUID) -> Client | None:
        """Get client by ID."""
        result = await self.session.execute(
            select(Client).where(Client.id == client_id)
        )
        return result.scalar_one_or_none()

    async def get_products_by_ids(self, product_ids: list[UUID]) -> list[Product]:
        """Get products by IDs."""
        result = await self.session.execute(
            select(Product).where(Product.id.in_(product_ids))
        )
        return result.scalars().all()

    async def create(self, order: Order, items: list[OrderItem]) -> Order:
        """Create new order."""
        self.session.add(order)
        self.session.add_all(items)
        await self.session.flush()
        await self.session.refresh(order)
        # load items to return
        stmt = (
            select(Order).options(selectinload(Order.items)).where(Order.id == order.id)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one()

    async def get_orders_by_client(self, client_id: UUID) -> list[Order]:
        """Get orders by client ID."""
        stmt = (
            select(Order)
            .options(selectinload(Order.items))
            .where(Order.client_id == client_id)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()
