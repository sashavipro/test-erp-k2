from fastapi import APIRouter
from typing import List
from uuid import UUID
from dishka.integrations.fastapi import FromDishka

from src.core.exceptions import create_error_responses, ClientNotFoundError, ProductNotFoundError
from src.apps.orders.schemas import OrderCreate, OrderResponse
from src.apps.orders.services import OrderService

router = APIRouter(prefix="/orders", tags=["orders"])

@router.post("/", response_model=OrderResponse, status_code=201, responses=create_error_responses(ClientNotFoundError, ProductNotFoundError))
async def create_order(order_in: OrderCreate, service: FromDishka[OrderService]):
    return await service.create_order(order_in)

@router.get("/client/{client_id}", response_model=List[OrderResponse], responses=create_error_responses(ClientNotFoundError))
async def get_orders_by_client(client_id: UUID, service: FromDishka[OrderService]):
    return await service.get_orders_for_client(client_id)
