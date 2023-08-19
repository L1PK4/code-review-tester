import enum
from typing import Optional

from pydantic import Field
from app.schemas.base import BaseSchema


class CreatingTelVerificationCode(BaseSchema):
    tel: str = Field(..., title="Телефон")


class UpdatingTelVerificationCode(BaseSchema):
    pass


class GettingTelVerificationCode(BaseSchema):
    code: str


class VerifyingTelCode(BaseSchema):
    tel: str = Field(..., title="Телефон")
    code: str = Field(..., title="Код подтверждения")
