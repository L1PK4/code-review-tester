import random
import uuid
from datetime import datetime, timedelta
from typing import Any

from jose import jwt
from passlib.context import CryptContext

from app.config import settings

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
ALGORITHM = 'HS256'


def generate_password_reset_token(email: str) -> str:
    delta = timedelta(hours=settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS)
    now = datetime.utcnow()
    expires = now + delta
    exp = expires.timestamp()
    encoded_jwt = jwt.encode(
        {'exp': exp, 'nbf': now, 'sub': email}, settings.SECRET_KEY, algorithm='HS256',
    )
    return encoded_jwt


def verify_password_reset_token(token: str) -> str | None:
    try:
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        return decoded_token['email']
    except jwt.JWTError:
        return None


def generate_random_password(length: int) -> str:
    """
    Генерирует стороку, содержащую пароль
    :param length: длина генерируемой стрпоки
    :return: псевдослучайная строка, составленная из латинских букв в нижнем и верхнем регистре и цифр заданной длины
    """
    alphabet = [
        '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B',
        'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N',
        'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k',
        'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x',
        'y', 'z'
    ]

    result = ''.join(random.choices(alphabet, k=length))

    return result


def create_token(
        subject: Any,
        expires_delta: timedelta | None = None,
        token_type: str | None = None,
        nbf: datetime | None = None,
        jti: str | None = None,
        **extra_args
) -> str:

    now = datetime.utcnow()

    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    claim_extra_fields: list[str] = getattr(settings, 'TOKEN_FIELDS', [])

    to_encode: dict[str, Any] = {
        "sub": str(subject),
        **extra_args
    }

    if "exp" in claim_extra_fields:
        to_encode["exp"] = expire
    if "iat" in claim_extra_fields:
        to_encode["iat"] = now
    if "nbf" in claim_extra_fields:
        to_encode["nbf"] = nbf if nbf is not None else now
    if "jti" in claim_extra_fields:
        to_encode["jti"] = jti if jti is not None else str(uuid.uuid4())

    if token_type is not None:
        to_encode["type"] = token_type
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)