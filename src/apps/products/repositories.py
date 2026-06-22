from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from uuid import UUID

from src.apps.products.models import Product
from src.apps.products.schemas import ProductCreate

class ProductRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self) -> List[Product]:
        result = await self.session.execute(select(Product))
        return result.scalars().all()

    async def get_by_id(self, product_id: UUID) -> Product | None:
        result = await self.session.execute(select(Product).where(Product.id == product_id))
        return result.scalar_one_or_none()

    async def create(self, product_in: ProductCreate) -> Product:
        product = Product(name=product_in.name, price=product_in.price)
        self.session.add(product)
        await self.session.flush()
        await self.session.refresh(product)
        return product
