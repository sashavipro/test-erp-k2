from fastapi import APIRouter
from typing import List
from uuid import UUID
from dishka.integrations.fastapi import FromDishka

from src.core.exceptions import create_error_responses, ClientNotFoundError
from src.apps.clients.schemas import ClientCreate, ClientResponse
from src.apps.clients.services import ClientService

router = APIRouter(prefix="/clients", tags=["clients"])

@router.get("/", response_model=List[ClientResponse])
async def get_clients(service: FromDishka[ClientService]):
    return await service.get_clients()

@router.post("/", response_model=ClientResponse, status_code=201)
async def create_client(client_in: ClientCreate, service: FromDishka[ClientService]):
    return await service.create_client(client_in)

@router.get("/{client_id}", response_model=ClientResponse, responses=create_error_responses(ClientNotFoundError))
async def get_client(client_id: UUID, service: FromDishka[ClientService]):
    return await service.get_client_by_id(client_id)
