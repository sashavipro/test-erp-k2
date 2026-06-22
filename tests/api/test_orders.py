"""tests/api/test_orders.py."""

import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio(loop_scope="session")


async def test_create_order(
    async_client: AsyncClient, create_client_fixture, create_product_fixture
):
    """Test creating a new order calculates total automatically."""
    from decimal import Decimal

    client = await create_client_fixture()
    product1 = await create_product_fixture(price=Decimal("10.00"))
    product2 = await create_product_fixture(price=Decimal("25.50"))

    order_data = {
        "client_id": str(client.id),
        "items": [
            {"product_id": str(product1.id), "quantity": 2},
            {"product_id": str(product2.id), "quantity": 1},
        ],
    }

    response = await async_client.post("/api/orders/", json=order_data)
    assert response.status_code == 201

    data = response.json()
    assert data["client_id"] == str(client.id)
    assert "id" in data
    # 10*2 + 25.50*1 = 45.50
    assert data["total_amount"] == "45.50"


async def test_create_order_client_not_found(
    async_client: AsyncClient, create_product_fixture
):
    """Test creating an order for a non-existent client."""
    from decimal import Decimal
    from uuid import uuid4

    product = await create_product_fixture(price=Decimal("10.00"))

    order_data = {
        "client_id": str(uuid4()),
        "items": [
            {"product_id": str(product.id), "quantity": 1},
        ],
    }

    response = await async_client.post("/api/orders/", json=order_data)
    assert response.status_code == 404
    assert response.json()["message"] == "Client not found"


async def test_create_order_product_not_found(
    async_client: AsyncClient, create_client_fixture
):
    """Test creating an order with a non-existent product."""
    from uuid import uuid4

    client = await create_client_fixture()

    order_data = {
        "client_id": str(client.id),
        "items": [
            {"product_id": str(uuid4()), "quantity": 1},
        ],
    }

    response = await async_client.post("/api/orders/", json=order_data)
    assert response.status_code == 404
    assert response.json()["message"] == "Product not found"


async def test_get_orders_for_client(
    async_client: AsyncClient,
    create_client_fixture,
    create_order_fixture,
    create_product_fixture,
    db_session,
):
    """Test retrieving orders for a specific client."""
    from decimal import Decimal

    from src.apps.orders.models import OrderItem

    client = await create_client_fixture()
    product = await create_product_fixture(price=Decimal("15.00"))

    order1 = await create_order_fixture(
        client_id=client.id, total_amount=Decimal("30.00")
    )
    # Add items to order
    item1 = OrderItem(order_id=order1.id, product_id=product.id, quantity=2)
    db_session.add(item1)

    order2 = await create_order_fixture(
        client_id=client.id, total_amount=Decimal("15.00")
    )
    item2 = OrderItem(order_id=order2.id, product_id=product.id, quantity=1)
    db_session.add(item2)

    await db_session.flush()

    response = await async_client.get(f"/api/orders/client/{client.id}")
    assert response.status_code == 200

    data = response.json()
    assert len(data) == 2

    # Verify order items are returned
    assert data[0]["total_amount"] == "30.00"
    assert len(data[0]["items"]) == 1
    assert data[0]["items"][0]["quantity"] == 2
