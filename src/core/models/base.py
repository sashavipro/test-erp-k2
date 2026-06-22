import datetime
import re
from typing import Annotated
from sqlalchemy import MetaData, func
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, mapped_column, declared_attr

POSTGRES_INDEXES_NAMING_CONVENTION = {
    "ix": "%(column_0_label)s_idx",
    "uq": "%(table_name)s_%(column_0_name)s_key",
    "ck": "%(table_name)s_%(constraint_name)s_check",
    "fk": "%(table_name)s_%(column_0_name)s_fkey",
    "pk": "%(table_name)s_pkey",
}

IntPK = Annotated[int, mapped_column(primary_key=True)]

CreatedAt = Annotated[
    datetime.datetime,
    mapped_column(server_default=func.now()),
]

UpdatedAt = Annotated[
    datetime.datetime,
    mapped_column(server_default=func.now(), onupdate=func.now()),
]

def camel_to_snake(name: str) -> str:
    name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()

class Base(AsyncAttrs, DeclarativeBase):
    """
    Base class for all SQLAlchemy models.
    Automatically generates __tablename__ and configures indexes.
    """

    metadata = MetaData(naming_convention=POSTGRES_INDEXES_NAMING_CONVENTION)

    @declared_attr.directive
    def __tablename__(cls) -> str:
        snake_case = camel_to_snake(cls.__name__)
        return f"{snake_case}s"
