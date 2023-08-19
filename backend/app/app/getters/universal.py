from typing import Type, TypeVar

from app.models.base_model import BaseModel
from app.schemas.base import BaseSchema


SchemaType = TypeVar("SchemaType", bound=BaseSchema)


def transform(db_obj: BaseModel, target_schema: Type[SchemaType], **kwargs) -> SchemaType:
    data = {}

    for key in db_obj.__table__.columns.keys():
        if key in target_schema.__fields__:
            data[key] = getattr(db_obj, key)

    data.update(kwargs)

    return target_schema(**data)
