import secrets
from typing import Any

from pydantic import AnyHttpUrl, BaseSettings, HttpUrl, PostgresDsn, validator


class Settings(BaseSettings):

    API_STR: str
    SECRET_KEY: str = secrets.token_urlsafe(32)
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    SERVER_NAME: str
    SERVER_HOST: AnyHttpUrl
    BACKEND_CORS_ORIGINS: Any = []

    @validator('BACKEND_CORS_ORIGINS', pre=True)
    def assemble_cors_origins(cls, v: str | list[str]) -> list[str] | str:
        if isinstance(v, str) and not v.startswith('['):
            return [i.strip() for i in v.split(',')]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    PROJECT_NAME: str
    SENTRY_DSN: HttpUrl | None = None

    @validator('SENTRY_DSN', pre=True)
    def sentry_dsn_can_be_blank(cls, v: str) -> str | None:
        if len(v) == 0:
            return None
        return v

    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    SQLALCHEMY_DATABASE_URI: PostgresDsn | None = None

    @validator('SQLALCHEMY_DATABASE_URI', pre=True)
    def assemble_db_connection(cls, v: str | None, values: dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme='postgresql',
            user=values.get('POSTGRES_USER'),
            password=values.get('POSTGRES_PASSWORD'),
            host=values.get('POSTGRES_SERVER'),
            path=f'/'+str(values.get('POSTGRES_DB') or ''),
        )

    SMTP_TLS: bool = True
    SMTP_PORT: int | None = None
    SMTP_HOST: str | None = None
    SMTP_USER: str | None = None
    SMTP_PASSWORD: str | None = None
    EMAILS_FROM_EMAIL: str | None = None
    EMAILS_FROM_NAME: str | None = None

    @validator('EMAILS_FROM_NAME')
    def get_project_name(cls, v: str | None, values: dict[str, Any]) -> str:
        if not v:
            return values['PROJECT_NAME']
        return v

    EMAILS_ENABLED: bool = False

    @validator('EMAILS_ENABLED', pre=True)
    def get_emails_enabled(cls, v: bool, values: dict[str, Any]) -> bool:
        return bool(
            values.get('SMTP_HOST')
            and values.get('SMTP_PORT')
            and values.get('EMAILS_FROM_EMAIL')
        )

    FIRST_SUPERUSER: str
    FIRST_SUPERUSER_PASSWORD: str
    TOKEN_FIELDS: list[str]

    S3_SERVICE_NAME: str | None = None
    S3_ENDPOINTS_URL: str | None = None
    S3_ACCESS_KEY_ID: str | None = None
    S3_SECRET_ACCESS_KEY: str | None = None
    S3_BUCKET_NAME: str | None = None

    GREENSMS_USER: str | None = None
    GREENSMS_PASSWORD: str | None = None

    class Config:
        case_sensitive = True

    SBER_USERNAME: str | None = None
    SBER_PASSWORD: str | None = None
    SBER_BASE_URL: str | None = None


settings = Settings()
