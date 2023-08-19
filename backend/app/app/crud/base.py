import logging
import os
import uuid
from typing import Any, Generic, Type, TypeVar

from app.models.base_model import BaseModel
from app.schemas.base import BaseSchema
from app.schemas.response import Paginator
from app.utils import pagination
from botocore.client import BaseClient
from fastapi import UploadFile
from sqlalchemy import inspect, orm
from sqlalchemy.orm import Session

ModelType = TypeVar('ModelType', bound=BaseModel)
CreatingSchemaType = TypeVar('CreatingSchemaType', bound=BaseSchema)
UpdatingSchemaType = TypeVar('UpdatingSchemaType', bound=BaseSchema)


class CRUDBase(Generic[ModelType, CreatingSchemaType, UpdatingSchemaType]):

    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get(self, db: Session, id: Any) -> ModelType | None:
        return db.query(self.model).filter(self.model.id == id).first()

    def get_many(self, db: Session, ids: list[Any]) -> list[ModelType]:
        return db.query(self.model).filter(self.model.id.in_(ids)).all()

    def _get_filter_by_name(self, name):
        return None

    def _filters(self, query: orm.Query, filters: dict[str, Any]) -> orm.Query:
        empty_filters = {}
        simple_filters = {}
        custom_filters = {}
        f_filters = []

        for name, value in filters.items():
            if value is None:
                empty_filters[name] = value
                continue
            f = self._get_filter_by_name(name)
            if f is not None:
                f_filters.append((f, value))
                continue
            model_info = inspect(self.model)
            if name in model_info.columns.keys() + model_info.relationships.keys():
                simple_filters[name] = value
            else:
                custom_filters[name] = value

        if len(simple_filters.keys()) > 0:
            query = query.filter_by(**simple_filters)
        for f, value in f_filters:
            query = f(query, value)
        return query

    def get_page(
            self,
            db: Session,
            order_by: Any | None = None,
            page: int | None = None,
            size: int = 30,
            **filers
    ) -> tuple[list[ModelType], Paginator]:
        query = db.query(self.model)
        if order_by is None:
            if hasattr(self.model, 'id'):
                query = query.order_by(self.model.id)
        else:
            query = query.order_by(order_by)
        query = self._filters(query, filers)
        return pagination.get_page(query, page, size=size)

    def get_multi(
        self, db: Session, skip: int = 0, limit: int = 30, order_by: Any | None = None, **filters
    ) -> list[ModelType]:
        query = db.query(self.model)
        if order_by is None:
            if hasattr(self.model, 'id'):
                query = query.order_by(self.model.id)
        else:
            query = query.order_by(order_by)
        query = query.offset(skip).limit(limit)
        query = self._filters(query, filters)
        return query.all()

    def _adapt_fields(self, obj: dict[str, Any] | BaseSchema, **kwargs) -> dict[str, Any]:
        if isinstance(obj, dict):
            data = obj
        else:
            data = obj.dict(exclude_unset=True)
        data.update(**kwargs)
        return data

    def _set_db_obj_fields(self, db_obj, fields):
        info = inspect(self.model)
        for field in info.columns.keys() + info.relationships.keys():
            if field in fields:
                setattr(db_obj, field, fields[field])
        return db_obj

    def create(self, db: Session, *, obj_in: CreatingSchemaType | dict[str, Any], **kwargs) -> ModelType:
        db_obj = self.model()
        fields = self._adapt_fields(obj_in, **kwargs)
        db_obj = self._set_db_obj_fields(db_obj=db_obj, fields=fields)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: UpdatingSchemaType | dict[str, Any],
        **kwargs
    ) -> ModelType:
        fields = self._adapt_fields(obj_in, **kwargs)
        db_obj = self._set_db_obj_fields(db_obj=db_obj, fields=fields)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def _remove(self, db: Session, *, obj: ModelType | None) -> ModelType | None:
        if obj is not None:
            db.delete(obj)
            return obj
        return None

    def remove_obj(self, db: Session, *, obj: ModelType | None):
        self._remove(db=db, obj=obj)
        db.commit()
        return None

    def remove_by_id(self, db: Session, *, id: Any) -> ModelType | None:
        return self.remove_obj(db=db, obj=self.get(db=db, id=id))

    def remove_many_obj(self, db: Session, *, objs: list[ModelType]) -> list[ModelType]:
        results = []
        for obj in objs:
            result = self._remove(db=db, obj=obj)
            if result is not None:
                results.append(result)
        db.commit()
        return results

    def remove_many_by_ids(self, db: Session, *, ids: list[Any]) -> list[ModelType]:
        return self.remove_many_obj(db=db, objs=self.get_many(db=db, ids=ids))
