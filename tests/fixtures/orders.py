"""tests/fixtures/orders.py."""

import uuid
from collections.abc import Callable
from decimal import Decimal

import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.orders.models import Order


@pytest_asyncio.fixture
async def create_order_fixture(db_session: AsyncSession) -> Callable:
    """Fixture factory to create a test order in the DB."""

    async def _create_order(
        client_id: uuid.UUID, total_amount: Decimal = Decimal("0.0")
    ) -> Order:
        order = Order(id=uuid.uuid4(), client_id=client_id, total_amount=total_amount)
        db_session.add(order)
        await db_session.flush()
        return order

    return _create_order
