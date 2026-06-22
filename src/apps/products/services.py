"""src/apps/products/services.py."""

from uuid import UUID

from src.apps.products.repositories import ProductRepository
from src.apps.products.schemas import ProductCreate
from src.apps.products.schemas import ProductResponse
from src.core.exceptions import ProductNotFoundError
from src.core.logger import logger


class ProductService:
    """Service class for managing Product-related business logic."""

    def __init__(self, repo: ProductRepository):
        """Initialize service."""
        self.repo = repo

    async def get_products(self) -> list[ProductResponse]:
        """Retrieve all products from the repository."""
        return await self.repo.get_all()

    async def create_product(self, product_in: ProductCreate) -> ProductResponse:
        """Create a new product with the provided details."""
        logger.info(f"Creating new product: {product_in.name}")
        return await self.repo.create(product_in)

    async def get_product_by_id(self, product_id: UUID) -> ProductResponse:
        """Retrieve a specific product by ID.

        Raises HTTP 404 if the product is not found.
        """
        product = await self.repo.get_by_id(product_id)
        if not product:
            raise ProductNotFoundError
        return product
