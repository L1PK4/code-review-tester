from .models import AuthSession
from .schemas import CreatingAuthSession, UpdatingAuthSession
from ...crud.base import CRUDBase


class CRUDAuthSession(CRUDBase[AuthSession, CreatingAuthSession, UpdatingAuthSession]):
    def _get_filter_by_name(self, name):
        match name:
            case "is_ended":
                return lambda query,value: query.filter((self.model.ended != None) == value)


auth_session = CRUDAuthSession(AuthSession)
