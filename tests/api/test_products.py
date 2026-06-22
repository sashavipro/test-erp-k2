"""tests/api/test_products.py."""

import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio(loop_scope="session")


async def test_get_products_empty(async_client: AsyncClient):
    """Test get products returns empty list initially."""
    response = await async_client.get("/api/products/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


async def test_create_product(async_client: AsyncClient):
    """Test creating a new product."""
    product_data = {"name": "Test Product", "price": "100.50"}
    response = await async_client.post("/api/products/", json=product_data)
    assert response.status_code == 201

    data = response.json()
    assert data["name"] == product_data["name"]
    assert data["price"] == "100.50"
    assert "id" in data


async def test_get_product(async_client: AsyncClient, create_product_fixture):
    """Test retrieving an existing product."""
    from decimal import Decimal

    product = await create_product_fixture(name="Laptop", price=Decimal("999.99"))

    response = await async_client.get(f"/api/products/{product.id}")
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == str(product.id)
    assert data["name"] == "Laptop"
    assert data["price"] == "999.99"


async def test_get_product_not_found(async_client: AsyncClient):
    """Test retrieving a non-existent product."""
    from uuid import uuid4

    response = await async_client.get(f"/api/products/{uuid4()}")
    assert response.status_code == 404
    assert response.json()["message"] == "Product not found"
