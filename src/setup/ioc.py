"""src/setup/ioc.py."""

from dishka import AsyncContainer
from dishka import make_async_container

from src.apps.clients.provider import ClientProvider
from src.apps.orders.provider import OrderProvider
from src.apps.products.provider import ProductProvider
from src.infrastructure.provider import InfraProvider


def create_container() -> AsyncContainer:
    """Build and return the Dishka DI container with all module providers."""
    return make_async_container(
        InfraProvider(), ClientProvider(), ProductProvider(), OrderProvider()
    )
