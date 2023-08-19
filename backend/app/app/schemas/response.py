from typing import TypeVar, Generic, Any

from pydantic import Field
from pydantic.generics import GenericModel

from app.schemas.base import BaseSchema


class Paginator(BaseSchema):
    page: int = Field(1, ge=1)
    total: int = Field(1, ge=0)
    has_prev: bool
    has_next: bool


class Error(BaseSchema):
    code: int = Field(0, ge=0, title="Код ошибки")
    message: str = Field(0, title="Человеко-читаемое сообщение")
    path: str = Field(None, title="местоположение")
    additional: Any


class Meta(BaseSchema):
    paginator: Paginator | None


class BaseResponse(BaseSchema):

    """Базовая структура ответа от сервера"""

    message: str = Field(default="Ok")
    meta: Meta = Field(default=Meta(paginator=None))
    errors: list[Error] = Field([])
    description: str = Field(default="Выполнено")


Entity = TypeVar('Entity')


class OkResponse(BaseResponse):
    """Ответ от сервера без полезной нагрузки"""
    data: None = None


class SingleEntityResponse(GenericModel, Generic[Entity], BaseResponse):
    """Ответ от сервера с одним объектом указанного типа"""
    data: Entity | None = Field(None)


class ListOfEntityResponse(GenericModel, Generic[Entity], BaseResponse):
    """Ответ от сервера со списком объектов указанного типа"""
    data: list[Entity] = Field([])
