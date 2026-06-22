"""src/apps/clients/repositories.py."""

from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.apps.clients.models import Client
from src.apps.clients.schemas import ClientCreate


class ClientRepository:
    """Client repository."""

    def __init__(self, session: AsyncSession):
        """Initialize repository."""
        self.session = session

    async def get_all(self) -> list[Client]:
        """Get all clients."""
        result = await self.session.execute(select(Client))
        return result.scalars().all()

    async def get_by_id(self, client_id: UUID) -> Client | None:
        """Get client by id."""
        result = await self.session.execute(
            select(Client).where(Client.id == client_id)
        )
        return result.scalar_one_or_none()

    async def create(self, client_in: ClientCreate) -> Client:
        """Create new client."""
        client = Client(name=client_in.name, email=client_in.email)
        self.session.add(client)
        await self.session.flush()
        await self.session.refresh(client)
        return client
