from .models import AuthSession
from .schemas import GettingAuthSession
from ..datetime import to_unix_timestamp
from ...getters import transform


def get_auth_session(auth_session: AuthSession, user) -> GettingAuthSession:

    if user is None:
        is_current = None
    elif not hasattr(user, 'auth_session'):
        is_current = None
    elif user.auth_session is None:
        is_current = None
    else:
        is_current = user.auth_session.id == auth_session.id

    return transform(
        db_obj=auth_session,
        target_schema=GettingAuthSession,
        created=to_unix_timestamp(auth_session.created),
        ended=to_unix_timestamp(auth_session.ended),
        last_activity=to_unix_timestamp(auth_session.created),
        is_current=is_current
    )
