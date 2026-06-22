"""src/apps/products/routers.py."""

from uuid import UUID

from dishka.integrations.fastapi import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter

from src.apps.products.schemas import ProductCreate
from src.apps.products.schemas import ProductResponse
from src.apps.products.services import ProductService
from src.core.exceptions import COMMON_ERROR_CLASSES
from src.core.exceptions import ProductNotFoundError
from src.core.exceptions import create_error_responses

router = APIRouter(
    prefix="/products",
    tags=["products"],
    responses=create_error_responses(*COMMON_ERROR_CLASSES),
)


@router.get("/", response_model=list[ProductResponse])
@inject
async def get_products(service: FromDishka[ProductService]):
    """Get products."""
    return await service.get_products()


@router.post("/", response_model=ProductResponse, status_code=201)
@inject
async def create_product(
    product_in: ProductCreate, service: FromDishka[ProductService]
):
    """Create product."""
    return await service.create_product(product_in)


@router.get(
    "/{product_id}",
    response_model=ProductResponse,
    responses=create_error_responses(ProductNotFoundError),
)
@inject
async def get_product(product_id: UUID, service: FromDishka[ProductService]):
    """Get product."""
    return await service.get_product_by_id(product_id)
