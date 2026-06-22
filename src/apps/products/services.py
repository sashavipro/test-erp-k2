from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID

from src.apps.products.schemas import ProductCreate, ProductResponse
from src.apps.products.repositories import ProductRepository
from src.core.exceptions import ProductNotFoundError
from src.core.logger import logger

class ProductService:
    """
    Service class for managing Product-related business logic.
    """
    def __init__(self, repo: ProductRepository):
        self.repo = repo

    async def get_products(self) -> List[ProductResponse]:
        """Retrieve all products from the repository."""
        return await self.repo.get_all()

    async def create_product(self, product_in: ProductCreate) -> ProductResponse:
        """Create a new product with the provided details."""
        logger.info(f"Creating new product: {product_in.name}")
        return await self.repo.create(product_in)

    async def get_product_by_id(self, product_id: UUID) -> ProductResponse:
        """
        Retrieve a specific product by ID.
        Raises HTTP 404 if the product is not found.
        """
        product = await self.repo.get_by_id(product_id)
        if not product:
            raise ProductNotFoundError()
        return product
