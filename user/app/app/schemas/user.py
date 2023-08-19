from pydantic import Field

from app.schemas.base import BaseSchema


# Shared properties
class BaseUser(BaseSchema):
    email: str | None = None
    tel: str | None = None
    is_active: bool | None = True
    is_superuser: bool = False
    full_name: str | None = None


# Properties to receive via API on creation
class CreatingUser(BaseUser):
    password: str | None = None


# Properties to receive via API on update
class UpdatingUser(BaseUser):
    password: str | None = None


class GettingUser(BaseUser):
    id: int | None = None
    last_activity: int | None = None


class EmailPasswordBody(BaseSchema):
    email: str
    password: str


class TelPasswordBody(BaseSchema):
    tel: str
    password: str


class TokenWithUser(BaseSchema):
    user: GettingUser
    token: str


class ExistsRequest(BaseSchema):
    email: str | None


class ExistsResponse(BaseSchema):
    exists: bool


class Registration(BaseSchema):
    code: str = Field(..., title="Код подтверждения")
    password: str = Field(..., title="Пароль")


class RegistrationByTel(Registration):
    tel: str = Field(..., title="Номер телефона")


class RegistrationByEmail(Registration):
    email: str = Field(..., title="Email")
