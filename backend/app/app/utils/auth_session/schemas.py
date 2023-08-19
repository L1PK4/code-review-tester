from app.schemas.base import BaseSchema


class AuthSessionInfo(BaseSchema):
    ip_address: str | None
    accept_language: str | None
    user_agent: str | None
    detected_os: str | None
    firebase_token: str | None


class CreatingAuthSession(BaseSchema):
    pass


class UpdatingAuthSession(BaseSchema):
    pass


class GettingAuthSession(AuthSessionInfo):
    id: int
    created: int
    ended: int | None
    last_activity: int
    is_current: bool | None
