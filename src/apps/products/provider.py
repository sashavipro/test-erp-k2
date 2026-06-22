from dishka import Provider, Scope, provide

from src.apps.products.repositories import ProductRepository
from src.apps.products.services import ProductService

class ProductProvider(Provider):
    product_repo = provide(ProductRepository, scope=Scope.REQUEST)
    product_service = provide(ProductService, scope=Scope.REQUEST)
