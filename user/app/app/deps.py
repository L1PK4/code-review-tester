import datetime
from typing import Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.config import settings
from app.services.email_sender import BaseEmailSender, SmtpEmailSender, FakeEmailSender
from app.services.payment.base_payment import BasePayment
from app.services.payment.fake_payment import FakePayment
from app.services.payment.sber_payment import SberPayment
from app.services.storage.base_storage import BaseStorage
from app.services.storage.s3_storage import S3Storage
from app.services.tel_verifier.base_tel_verifier import BaseTelVerifier
from app.services.tel_verifier.fake_tel_verifier import FakeTelVerifier
from app.session import SessionLocal
import boto3
from app.utils import security

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f'{settings.API_STR}/login/access-token'
)
optional_reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f'{settings.API_STR}/login/access-token',
    auto_error=False
)


def get_db() -> Generator:
    db = None
    try:
        db = SessionLocal()
        yield db
    finally:
        if db is not None:
            db.close()


def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> models.User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = schemas.TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
    user = crud.user.get(db, id=token_data.sub)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    user.jwt_payload = payload
    if hasattr(user, 'last_activity'):
        user.last_activity = datetime.datetime.utcnow()
        db.add(user)
        db.commit()
    return user


def get_current_active_user(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    if not current_user.is_active:
        raise HTTPException(status_code=403, detail="Inactive user")
    return current_user


def get_current_active_superuser(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=403, detail="The user doesn't have enough privileges"
        )
    return current_user


def get_bucket_name() -> str | None:
    return settings.S3_BUCKET_NAME


def get_s3_client():
    session = boto3.session.Session()
    s3 = session.client(
        service_name=settings.S3_SERVICE_NAME,
        endpoint_url=settings.S3_ENDPOINTS_URL,
        aws_access_key_id=settings.S3_ACCESS_KEY_ID,
        aws_secret_access_key=settings.S3_SECRET_ACCESS_KEY,
    )

    return s3


def get_email_sender() -> BaseEmailSender:
    # sender = TelegramEmailSender(bot_token=settings.ERROR_NOTIFIER_TOKEN,recipients=settings.ERROR_NOTIFIER_RECIPIENTS)
    sender = FakeEmailSender()
    return sender


def get_tel_verifier() -> BaseTelVerifier:
    verifier = FakeTelVerifier()
    return verifier


def get_storage() -> BaseStorage:
    return S3Storage(
        bucket_name=settings.S3_BUCKET_NAME,
        service_name=settings.S3_SERVICE_NAME,
        endpoints_url=settings.S3_ENDPOINTS_URL,
        access_key_id=settings.S3_ACCESS_KEY_ID,
        secret_access_key=settings.S3_SECRET_ACCESS_KEY,
    )


def get_payment_service() -> BasePayment:
    # return SberPayment(
    #     user_name=settings.SBER_USER_NAME,
    #     password=settings.SBER_PASSWORD,
    #     base_url=settings.SBER_BASE_URL
    # )
    return FakePayment()
