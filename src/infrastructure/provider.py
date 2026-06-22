"""src/infrastructure/provider.py."""

from collections.abc import AsyncIterable

from dishka import Provider
from dishka import Scope
from dishka import provide
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.logger import logger
from src.infrastructure.database import async_session_maker


class InfraProvider(Provider):
    """Infrastructure provider."""

    @provide(scope=Scope.REQUEST)
    async def get_session(self) -> AsyncIterable[AsyncSession]:
        """Provide a database session for the request scope with auto commit."""
        async with async_session_maker() as session:
            try:
                yield session
                await session.commit()
            except Exception as e:
                logger.error(
                    f"Database transaction failed: {e}. Rolling back.", exc_info=True
                )
                await session.rollback()
                raise
