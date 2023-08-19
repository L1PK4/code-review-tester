from datetime import datetime

from sqlalchemy import Boolean, Column, Integer, String, Enum, DateTime
from sqlalchemy.orm import relationship

from app.models.base_model import BaseModel


class EmailVerificationCode(BaseModel):

    id = Column(Integer, primary_key=True, index=True)

    email = Column(String, nullable=False)
    created = Column(DateTime(), nullable=False, default=datetime.utcnow)
    value = Column(String(), nullable=False)
    used = Column(Boolean(), nullable=False, default=False)
