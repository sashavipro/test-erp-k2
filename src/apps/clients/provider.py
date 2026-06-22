from dishka import Provider, Scope, provide

from src.apps.clients.repositories import ClientRepository
from src.apps.clients.services import ClientService

class ClientProvider(Provider):
    client_repo = provide(ClientRepository, scope=Scope.REQUEST)
    client_service = provide(ClientService, scope=Scope.REQUEST)
