"""src/apps/products/provider.py."""

from dishka import Provider
from dishka import Scope
from dishka import provide

from src.apps.products.repositories import ProductRepository
from src.apps.products.services import ProductService


class ProductProvider(Provider):
    """Product provider."""

    product_repo = provide(ProductRepository, scope=Scope.REQUEST)
    product_service = provide(ProductService, scope=Scope.REQUEST)
