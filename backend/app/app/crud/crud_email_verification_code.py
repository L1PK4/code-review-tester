from datetime import datetime, timedelta
from typing import Any, Dict, Optional, Union

from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.email_verification_code import EmailVerificationCode
from app.schemas.base import BaseSchema
from app.schemas.email_verification_code import CreatingEmailVerificationCode, UpdatingEmailVerificationCode, VerifyingEmailCode
from app.utils.code import fake_gen


class CRUDEmailVerificationCode(CRUDBase[EmailVerificationCode, CreatingEmailVerificationCode, UpdatingEmailVerificationCode]):

    def _adapt_fields(self, obj: dict[str, Any] | BaseSchema, **kwargs) -> dict[str, Any]:
        fields = super(CRUDEmailVerificationCode, self)._adapt_fields(obj=obj, **kwargs)
        if 'value' not in fields:
            fields['value'] = fake_gen(5)
        return fields

    def check_verification_code(self, db: Session, *, data: VerifyingEmailCode) -> int:

        model = self.model

        code = db.query(model)\
            .filter(model.email == data.email)\
            .order_by(model.used, desc(model.created))\
            .first()
        if code is None:
            return -3
        if code.used:
            return -1
        if datetime.utcnow() - code.created > timedelta(minutes=5):
            return -2
        if data.code != code.value:
            return -4
        else:
            code.used = True
            db.add(code)
            db.commit()
            return 0


email_verification_code = CRUDEmailVerificationCode(EmailVerificationCode)
