"""src/apps/clients/schemas.py."""

from uuid import UUID

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import EmailStr


class ClientBase(BaseModel):
    """Client base schema."""

    name: str
    email: EmailStr | None = None


class ClientCreate(ClientBase):
    """Client create schema."""


class ClientResponse(ClientBase):
    """Client response schema."""

    id: UUID

    model_config = ConfigDict(from_attributes=True)
