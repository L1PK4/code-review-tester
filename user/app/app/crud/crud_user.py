import datetime
from typing import Any

from app.schemas.base import BaseSchema
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.user import User
from app.schemas.user import CreatingUser, UpdatingUser, ExistsRequest, ExistsResponse
from app.utils.security import get_password_hash, verify_password


class CRUDUser(CRUDBase[User, CreatingUser, UpdatingUser]):

    def _adapt_fields(self, obj: dict[str, Any] | BaseSchema, **kwargs) -> dict[str, Any]:
        fields = super(CRUDUser, self)._adapt_fields(obj, **kwargs)
        if 'email' in fields:
            fields['email'] = fields['email'].lower() if isinstance(fields['email'], str) else fields['email']
        if 'password' in fields:
            fields['hashed_password'] = get_password_hash(fields.pop('password'))
        return fields

    def create(self, db: Session, *, obj_in: CreatingUser | dict[str, Any], **kwargs) -> User:
        fields = self._adapt_fields(obj_in, **kwargs)
        return super(CRUDUser, self).create(db=db, obj_in=fields)

    def update(
            self, db: Session, *, db_obj: User, obj_in: UpdatingUser | dict[str, Any], **kwargs
    ) -> User:
        fields = self._adapt_fields(obj_in, **kwargs)
        return super().update(db, db_obj=db_obj, obj_in=fields)

    def authenticate(self, db: Session, *, email: str | None = None, tel: str | None = None,
                     password: str | None = None) -> User | None:
        user = None

        attrs = {}

        if email is not None:
            attrs['email'] = email
        if tel is not None:
            attrs['tel'] = tel
        if len(attrs) > 0:
            user = self.get_by_attrs(db, **attrs)
        if not user:
            return None
        if password is not None and not verify_password(password, user.hashed_password):
            return None
        return user

    def exists(self, db: Session, *, data: ExistsRequest) -> ExistsResponse:
        return ExistsResponse(
            exists=db.query(self.model)
                       .filter_by(**data.dict(exclude_unset=True, exclude_none=True))
                       .first() is not None
        )

    def get_by_attrs(self, db: Session, auto_create: bool = False, **attrs) -> User | None:
        user = db.query(self.model).filter_by(**attrs).first()
        if user is not None:
            return user
        if not auto_create:
            return None
        return self._set_db_obj_fields(self.model(), attrs)

    def sign_out(self, db:Session, user: User) -> None:
        if user.auth_session is not None:
            user.auth_session.ended = datetime.datetime.utcnow()
            db.add(user.auth_session)
            db.commit()


user = CRUDUser(User)
