"""tests/conftest.py."""

import asyncio
from collections.abc import AsyncGenerator
from collections.abc import AsyncIterable

import httpx
import pytest
import pytest_asyncio
from dishka import AsyncContainer
from dishka import Provider
from dishka import Scope
from dishka import make_async_container
from dishka import provide
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker

from src.apps.clients.provider import ClientProvider
from src.apps.orders.provider import OrderProvider
from src.apps.products.provider import ProductProvider
from src.core.models.base import Base
from src.infrastructure.database import engine
from src.main import app

pytest_plugins = [
    "tests.fixtures.clients",
    "tests.fixtures.products",
    "tests.fixtures.orders",
]


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the whole session."""
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_db() -> AsyncGenerator[None, None]:
    """Create all database tables before tests."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


@pytest_asyncio.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """Provide a transactional database session that rolls back after the test."""
    async with engine.connect() as conn:
        trans = await conn.begin()

        session_maker = async_sessionmaker(
            bind=conn,
            class_=AsyncSession,
            expire_on_commit=False,
            join_transaction_mode="create_savepoint",
        )

        async with session_maker() as session:
            yield session

        await trans.rollback()


class TestInfraProvider(Provider):
    """Test infrastructure provider overriding database session."""

    def __init__(self, session: AsyncSession):
        super().__init__()
        self._session = session

    @provide(scope=Scope.REQUEST)
    async def get_session(self) -> AsyncIterable[AsyncSession]:
        """Provide the injected test session."""
        try:
            yield self._session
            await self._session.commit()
        except Exception:
            await self._session.rollback()
            raise


@pytest.fixture
def app_container(db_session: AsyncSession) -> AsyncContainer:
    """Create a test DI container."""
    return make_async_container(
        TestInfraProvider(db_session),
        ClientProvider(),
        ProductProvider(),
        OrderProvider(),
    )


@pytest_asyncio.fixture
async def async_client(
    app_container: AsyncContainer,
) -> AsyncGenerator[httpx.AsyncClient, None]:
    """Provide an HTTP test client."""
    app.state.dishka_container = app_container
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
