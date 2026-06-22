from dishka import Provider, Scope, provide

from src.apps.orders.repositories import OrderRepository
from src.apps.orders.services import OrderService

class OrderProvider(Provider):
    order_repo = provide(OrderRepository, scope=Scope.REQUEST)
    order_service = provide(OrderService, scope=Scope.REQUEST)
