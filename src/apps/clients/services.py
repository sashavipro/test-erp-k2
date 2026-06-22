from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID

from src.apps.clients.schemas import ClientCreate, ClientResponse
from src.apps.clients.repositories import ClientRepository
from src.core.exceptions import ClientNotFoundError
from src.core.logger import logger

class ClientService:
    """
    Service class for managing Client-related business logic.
    """
    def __init__(self, repo: ClientRepository):
        self.repo = repo

    async def get_clients(self) -> List[ClientResponse]:
        """Retrieve all clients from the repository."""
        return await self.repo.get_all()

    async def create_client(self, client_in: ClientCreate) -> ClientResponse:
        """Create a new client with the provided details."""
        logger.info(f"Creating new client: {client_in.name}")
        return await self.repo.create(client_in)

    async def get_client_by_id(self, client_id: UUID) -> ClientResponse:
        """
        Retrieve a specific client by ID.
        Raises HTTP 404 if the client is not found.
        """
        client = await self.repo.get_by_id(client_id)
        if not client:
            raise ClientNotFoundError()
        return client
