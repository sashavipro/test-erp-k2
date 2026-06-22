"""tests/fixtures/clients.py."""

import uuid
from collections.abc import Callable

import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.clients.models import Client


@pytest_asyncio.fixture
async def create_client_fixture(db_session: AsyncSession) -> Callable:
    """Fixture factory to create a test client in the DB."""

    async def _create_client(
        name: str = "Test Client", email: str = "test@example.com"
    ) -> Client:
        client = Client(id=uuid.uuid4(), name=name, email=email)
        db_session.add(client)
        await db_session.flush()
        return client

    return _create_client
