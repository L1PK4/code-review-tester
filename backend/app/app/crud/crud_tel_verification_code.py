from datetime import datetime, timedelta
from typing import Any

from app.crud.base import CRUDBase
from app.models.tel_verification_code import TelVerificationCode
from app.schemas.base import BaseSchema
from app.schemas.tel_verification_code import (CreatingTelVerificationCode,
                                               UpdatingTelVerificationCode,
                                               VerifyingTelCode)
from sqlalchemy import desc
from sqlalchemy.orm import Session


class CRUDTelVerificationCode(CRUDBase[TelVerificationCode, CreatingTelVerificationCode, UpdatingTelVerificationCode]):

    def _adapt_fields(self, obj: dict[str, Any] | BaseSchema, **kwargs) -> dict[str, Any]:
        fields = super(CRUDTelVerificationCode, self)._adapt_fields(obj=obj, **kwargs)
        if 'value' not in fields:
            fields['value'] = '8085'
        return fields

    def check_verification_code(self, db: Session, *, data: VerifyingTelCode) -> int:

        model = self.model

        code = db.query(model)\
            .filter(model.tel == data.tel)\
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


tel_verification_code = CRUDTelVerificationCode(TelVerificationCode)
