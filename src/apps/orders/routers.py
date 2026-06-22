"""src/apps/orders/routers.py."""

from uuid import UUID

from dishka.integrations.fastapi import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter

from src.apps.orders.schemas import OrderCreate
from src.apps.orders.schemas import OrderResponse
from src.apps.orders.services import OrderService
from src.core.exceptions import COMMON_ERROR_CLASSES
from src.core.exceptions import ClientNotFoundError
from src.core.exceptions import ProductNotFoundError
from src.core.exceptions import create_error_responses

router = APIRouter(
    prefix="/orders",
    tags=["orders"],
    responses=create_error_responses(*COMMON_ERROR_CLASSES),
)


@router.post(
    "/",
    response_model=OrderResponse,
    status_code=201,
    responses=create_error_responses(ClientNotFoundError, ProductNotFoundError),
)
@inject
async def create_order(order_in: OrderCreate, service: FromDishka[OrderService]):
    """Create order."""
    return await service.create_order(order_in)


@router.get(
    "/client/{client_id}",
    response_model=list[OrderResponse],
    responses=create_error_responses(ClientNotFoundError),
)
@inject
async def get_orders_by_client(client_id: UUID, service: FromDishka[OrderService]):
    """Get orders by client."""
    return await service.get_orders_for_client(client_id)
