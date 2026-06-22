"""src/apps/orders/provider.py."""

from dishka import Provider
from dishka import Scope
from dishka import provide

from src.apps.orders.repositories import OrderRepository
from src.apps.orders.services import OrderService


class OrderProvider(Provider):
    """Order provider."""

    order_repo = provide(OrderRepository, scope=Scope.REQUEST)
    order_service = provide(OrderService, scope=Scope.REQUEST)
