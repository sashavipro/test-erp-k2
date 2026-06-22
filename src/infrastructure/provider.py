from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncIterable

from src.infrastructure.database import async_session_maker
from src.core.logger import logger

class InfraProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def get_session(self) -> AsyncIterable[AsyncSession]:
        """Provides a database session for the request scope with auto commit/rollback."""
        async with async_session_maker() as session:
            try:
                yield session
                await session.commit()
            except Exception as e:
                logger.error(f"Database transaction failed: {e}. Rolling back.", exc_info=True)
                await session.rollback()
                raise
