from pydantic import BaseModel, EmailStr, ConfigDict
from uuid import UUID

class ClientBase(BaseModel):
    name: str
    email: EmailStr | None = None

class ClientCreate(ClientBase):
    pass

class ClientResponse(ClientBase):
    id: UUID

    model_config = ConfigDict(from_attributes=True)
