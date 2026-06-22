"""tests/test_main.py."""

from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


def test_app_title():
    """Test app title."""
    assert app.title == "test-erp-k2"


def test_api_clients_route_exists():
    """Test api clients route exists."""
    # Just checking if the route exists, avoiding DB execution
    found = False
    for route in app.routes:
        if getattr(route, "path", None) == "/api/clients/":
            found = True
            break
    assert found
