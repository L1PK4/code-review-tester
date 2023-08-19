import datetime

from fastapi import Header, Depends, HTTPException
from starlette.requests import Request
from user_agents import parse

from .models import AuthSession
from .schemas import AuthSessionInfo
from ...deps import get_db


def get_auth_session_info(
        request: Request,
        x_real_ip: str | None = Header(None),
        accept_language: str | None = Header(None),
        user_agent: str | None = Header(None),
        x_firebase_token: str | None = Header(None)
) -> AuthSessionInfo:
    detected_os = None

    if user_agent is not None:
        ua_string = str(user_agent)
        ua_object = parse(ua_string)

        detected_os = ua_object.os.family
        if detected_os is None or detected_os.lower() == 'other':
            if 'okhttp' in user_agent.lower():
                detected_os = 'Android'
            elif 'cfnetwork' in user_agent.lower():
                detected_os = 'iOS'
            else:
                detected_os = None

    return AuthSessionInfo(
        ip_address=x_real_ip if x_real_ip is not None else request.client.host,
        firebase_token=x_firebase_token,
        accept_language=accept_language,
        detected_os=detected_os,
        user_agent=user_agent,
    )


def in_auth_session(user_deps):
    def func(
            user=Depends(user_deps),
            auth_session_info: AuthSessionInfo = Depends(get_auth_session_info),
            db=Depends(get_db)
    ):
        if user is None:
            return None
        print(user.jwt_payload)
        session_id = user.jwt_payload.get('session_id', None) if user.jwt_payload is not None else None
        if session_id is not None:
            auth_session: AuthSession | None = db.query(AuthSession).get(session_id)
        else:
            auth_session = None
        if auth_session is None or auth_session.ended is not None:
            raise HTTPException(status_code=401, detail="Неактивный сеанс")

        auth_session.last_activity = datetime.datetime.utcnow()
        auth_session.firebase_token = auth_session_info.firebase_token
        db.add(auth_session)
        db.commit()
        user.auth_session = auth_session

        return user

    return func
