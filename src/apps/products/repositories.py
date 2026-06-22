"""src/apps/products/repositories.py."""

from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.apps.products.models import Product
from src.apps.products.schemas import ProductCreate


class ProductRepository:
    """Product repository."""

    def __init__(self, session: AsyncSession):
        """Initialize repository."""
        self.session = session

    async def get_all(self) -> list[Product]:
        """Get all products."""
        result = await self.session.execute(select(Product))
        return result.scalars().all()

    async def get_by_id(self, product_id: UUID) -> Product | None:
        """Get product by id."""
        result = await self.session.execute(
            select(Product).where(Product.id == product_id)
        )
        return result.scalar_one_or_none()

    async def create(self, product_in: ProductCreate) -> Product:
        """Create new product."""
        product = Product(name=product_in.name, price=product_in.price)
        self.session.add(product)
        await self.session.flush()
        await self.session.refresh(product)
        return product
