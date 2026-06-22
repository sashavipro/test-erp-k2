"""src/apps/clients/routers.py."""

from uuid import UUID

from dishka.integrations.fastapi import FromDishka
from fastapi import APIRouter

from src.apps.clients.schemas import ClientCreate
from src.apps.clients.schemas import ClientResponse
from src.apps.clients.services import ClientService
from src.core.exceptions import ClientNotFoundError
from src.core.exceptions import create_error_responses

router = APIRouter(prefix="/clients", tags=["clients"])


@router.get("/", response_model=list[ClientResponse])
async def get_clients(service: FromDishka[ClientService]):
    """Get clients."""
    return await service.get_clients()


@router.post("/", response_model=ClientResponse, status_code=201)
async def create_client(client_in: ClientCreate, service: FromDishka[ClientService]):
    """Create client."""
    return await service.create_client(client_in)


@router.get(
    "/{client_id}",
    response_model=ClientResponse,
    responses=create_error_responses(ClientNotFoundError),
)
async def get_client(client_id: UUID, service: FromDishka[ClientService]):
    """Get client."""
    return await service.get_client_by_id(client_id)
