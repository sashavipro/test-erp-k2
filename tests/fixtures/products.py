"""tests/fixtures/products.py."""

import uuid
from collections.abc import Callable
from decimal import Decimal

import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.products.models import Product


@pytest_asyncio.fixture
async def create_product_fixture(db_session: AsyncSession) -> Callable:
    """Fixture factory to create a test product in the DB."""

    async def _create_product(
        name: str = "Test Product", price: Decimal = Decimal("10.0")
    ) -> Product:
        product = Product(id=uuid.uuid4(), name=name, price=price)
        db_session.add(product)
        await db_session.flush()
        return product

    return _create_product
