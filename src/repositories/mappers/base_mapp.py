from typing import TypeVar

from pydantic import BaseModel

from src.database import Base

DBModelType = TypeVar("DBModelType", bound=Base)
SchemasType = TypeVar("SchemasType", bound=BaseModel)


class DataMapper:
    db_model: type[DBModelType] = None
    schemas: type[SchemasType] = None

    @classmethod
    def map_to_domain_entity(cls, data):
        return cls.schemas.model_validate(data, from_attributes=True)

    @classmethod
    def map_to_persistence_entity(cls, data):
        return cls.db_model(**data.model_dump())
