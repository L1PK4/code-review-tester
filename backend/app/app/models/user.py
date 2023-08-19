from typing import Any

from sqlalchemy import Boolean, Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

from app.models.base_model import BaseModel
from app.utils.auth_session.models import AuthSessionMixin


class User(BaseModel, AuthSessionMixin):
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=True)
    tel = Column(String, unique=True, index=True, nullable=True)
    hashed_password = Column(String, nullable=True)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)
    last_activity = Column(DateTime, nullable=True)

    auth_sessions = relationship('AuthSession', back_populates='user', passive_deletes=True, cascade="all, delete-orphan")

