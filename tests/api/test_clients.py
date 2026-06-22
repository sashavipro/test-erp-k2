"""tests/api/test_clients.py."""

import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio(loop_scope="session")


async def test_get_clients_empty(async_client: AsyncClient):
    """Test get clients returns empty list initially."""
    response = await async_client.get("/api/clients/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


async def test_create_client(async_client: AsyncClient):
    """Test creating a new client."""
    client_data = {"name": "Test Client", "email": "test@example.com"}
    response = await async_client.post("/api/clients/", json=client_data)
    assert response.status_code == 201

    data = response.json()
    assert data["name"] == client_data["name"]
    assert data["email"] == client_data["email"]
    assert "id" in data


async def test_get_client(async_client: AsyncClient, create_client_fixture):
    """Test retrieving an existing client."""
    client = await create_client_fixture(name="John Doe", email="john@example.com")

    response = await async_client.get(f"/api/clients/{client.id}")
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == str(client.id)
    assert data["name"] == "John Doe"
    assert data["email"] == "john@example.com"


async def test_get_client_not_found(async_client: AsyncClient):
    """Test retrieving a non-existent client."""
    from uuid import uuid4

    response = await async_client.get(f"/api/clients/{uuid4()}")
    assert response.status_code == 404
    assert response.json()["message"] == "Client not found"
