from dishka import make_async_container, AsyncContainer

from src.infrastructure.provider import InfraProvider
from src.apps.clients.provider import ClientProvider
from src.apps.products.provider import ProductProvider
from src.apps.orders.provider import OrderProvider

def create_container() -> AsyncContainer:
    """
    Builds and returns the Dishka DI container with all module providers.
    """
    return make_async_container(
        InfraProvider(),
        ClientProvider(),
        ProductProvider(),
        OrderProvider()
    )
