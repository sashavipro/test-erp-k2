"""src/apps/clients/provider.py."""

from dishka import Provider
from dishka import Scope
from dishka import provide

from src.apps.clients.repositories import ClientRepository
from src.apps.clients.services import ClientService


class ClientProvider(Provider):
    """Client provider."""

    client_repo = provide(ClientRepository, scope=Scope.REQUEST)
    client_service = provide(ClientService, scope=Scope.REQUEST)
