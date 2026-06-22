import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch

from src.main import app
from src.infrastructure.database import get_db_session

client = TestClient(app)

def test_app_title():
    assert app.title == "test-erp-k2"

def test_api_clients_route_exists():
    # Just checking if the route exists, avoiding DB execution
    found = False
    for route in app.routes:
        if getattr(route, "path", None) == "/api/clients/":
            found = True
            break
    assert found
