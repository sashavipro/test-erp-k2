from fastapi import APIRouter
from typing import List
from uuid import UUID
from dishka.integrations.fastapi import FromDishka

from src.core.exceptions import create_error_responses, ProductNotFoundError
from src.apps.products.schemas import ProductCreate, ProductResponse
from src.apps.products.services import ProductService

router = APIRouter(prefix="/products", tags=["products"])

@router.get("/", response_model=List[ProductResponse])
async def get_products(service: FromDishka[ProductService]):
    return await service.get_products()

@router.post("/", response_model=ProductResponse, status_code=201)
async def create_product(product_in: ProductCreate, service: FromDishka[ProductService]):
    return await service.create_product(product_in)

@router.get("/{product_id}", response_model=ProductResponse, responses=create_error_responses(ProductNotFoundError))
async def get_product(product_id: UUID, service: FromDishka[ProductService]):
    return await service.get_product_by_id(product_id)
