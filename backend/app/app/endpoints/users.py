from typing import Literal

from fastapi import APIRouter, Query, Depends, Path
from sqlalchemy.orm import Session

from app import crud, schemas, getters, deps, models
from app.exceptions import UnfoundEntity
from app.utils.auth_session.deps import in_auth_session
from app.utils.auth_session.schemas import GettingAuthSession
from app.utils.response import get_responses_description_by_codes

from app.utils.logging import lprint

router = APIRouter()


@router.get(
    '/cp/users/exists/',
    tags=["Панель Управления / Пользователи"],
    name="Проверить на существование пользователя",
    response_model=schemas.response.SingleEntityResponse[schemas.user.ExistsResponse],
    responses=get_responses_description_by_codes([401, 403, 400])
)
def check_user(
        email: str | None = Query(None),
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(in_auth_session(deps.get_current_active_superuser))
):
    exists = crud.crud_user.user.exists(db=db, data=schemas.user.ExistsRequest(email=email))

    return schemas.response.SingleEntityResponse(
        data=exists
    )


@router.get(
    '/cp/users/me/',
    tags=["Панель Управления / Профиль"],
    name="Получить текущего пользователя",
    response_model=schemas.response.SingleEntityResponse[schemas.user.GettingUser],
    responses=get_responses_description_by_codes([401, 403])
)
def get_user_by_id(
        current_user: models.User = Depends(in_auth_session(deps.get_current_active_superuser)),
):
    return schemas.response.SingleEntityResponse(
        data=getters.user.get_user(user=current_user)
    )


@router.put(
    '/cp/users/me/',
    tags=["Панель Управления / Профиль"],
    name="изменить текущего пользователя",
    response_model=schemas.response.SingleEntityResponse[schemas.user.GettingUser],
    responses=get_responses_description_by_codes([401, 403, 400])
)
def edit_user(
        data: schemas.user.UpdatingUser,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(in_auth_session(deps.get_current_active_superuser))
):
    user = crud.crud_user.user.update(db=db, db_obj=current_user, obj_in=data)

    return schemas.response.SingleEntityResponse(
        data=getters.user.get_user(user=user)
    )


@router.delete(
    '/cp/users/me/',
    tags=["Панель Управления / Профиль"],
    name="удалить текущего пользователя",
    response_model=schemas.response.OkResponse,
    responses=get_responses_description_by_codes([401, 403])
)
def edit_user(
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(in_auth_session(deps.get_current_active_superuser))
):
    crud.crud_user.user.remove_obj(db=db, obj=current_user)
    return schemas.response.OkResponse()


@router.get(
    '/cp/users/',
    tags=["Панель Управления / Пользователи"],
    name="Получить всех пользователей",
    response_model=schemas.response.ListOfEntityResponse[schemas.user.GettingUser],
    responses=get_responses_description_by_codes([401, 403, 400])
)
def get_all_users(
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(in_auth_session(deps.get_current_active_superuser)),
        is_active: bool | None = Query(None),
        is_superuser: bool | None = Query(None),
        page: int | None = Query(None)
):
    data, paginator = crud.crud_user.user.get_page(db=db, pag=page, is_active=is_active, is_superuser=is_superuser)

    return schemas.response.ListOfEntityResponse(
        data=[
            getters.user.get_user(user=user)
            for user in data
        ],
        meta=schemas.response.Meta(paginator=paginator)
    )


@router.get(
    '/cp/users/{user_id}/',
    tags=["Панель Управления / Пользователи"],
    name="Получить пользователя по идентификатору",
    response_model=schemas.response.SingleEntityResponse[schemas.user.GettingUser],
    responses=get_responses_description_by_codes([401, 403, 400, 404])
)
def get_user_by_id(
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(in_auth_session(deps.get_current_active_superuser)),
        user_id: int = Path(...)
):
    user = crud.crud_user.user.get(db=db, id=user_id)
    if user is None:
        raise UnfoundEntity(message="Пользователь не найден", num=1)

    return schemas.response.SingleEntityResponse(
        data=getters.user.get_user(user=user)
    )


@router.post(
    '/cp/users/',
    tags=["Панель Управления / Пользователи"],
    name="создать пользователя",
    response_model=schemas.response.SingleEntityResponse[schemas.user.GettingUser],
    responses=get_responses_description_by_codes([401, 403, 400])
)
def create_user(
        data: schemas.user.CreatingUser,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(in_auth_session(deps.get_current_active_superuser)),
):
    user = crud.crud_user.user.create(db=db, obj_in=data)

    return schemas.response.SingleEntityResponse(
        data=getters.user.get_user(user=user)
    )


@router.put(
    '/cp/users/{user_id}/',
    tags=["Панель Управления / Пользователи"],
    name="изменить пользователя",
    response_model=schemas.response.SingleEntityResponse[schemas.user.GettingUser],
    responses=get_responses_description_by_codes([401, 403, 400, 404])
)
def edit_user(
        data: schemas.user.UpdatingUser,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(in_auth_session(deps.get_current_active_superuser)),
        user_id: int = Path(...),
):
    user = crud.crud_user.user.get(db=db, id=user_id)
    if user is None:
        raise UnfoundEntity(message="Пользователь не найден", num=1)

    user = crud.crud_user.user.update(db=db, db_obj=user, obj_in=data)

    return schemas.response.SingleEntityResponse(
        data=getters.user.get_user(user=user)
    )


@router.delete(
    '/cp/users/{user_id}/',
    tags=["Панель Управления / Пользователи"],
    name="удалить пользователя",
    response_model=schemas.response.OkResponse,
    responses=get_responses_description_by_codes([401, 403, 400])
)
def edit_user(
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(in_auth_session(deps.get_current_active_superuser)),
        user_id: int = Path(...),
):
    crud.crud_user.user.remove_by_id(db=db, id=user_id)

    return schemas.response.OkResponse()


@router.get(
    '/cp/users/{user_id}/sessions/',
    tags=["Панель Управления / Пользователи"],
    name="Получить сеансы пользователя по идентификатору",
    response_model=schemas.response.ListOfEntityResponse[GettingAuthSession],
    responses=get_responses_description_by_codes([401, 403, 400, 404])
)
def get_auth_session_by_user_id(
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(in_auth_session(deps.get_current_active_superuser)),
        user_id: int | Literal["me"] = Path(...),
        page: int | None = Query(None)
):
    if user_id in ("me", 0, current_user.id):
        user = current_user
        is_current = True
    else:
        user = crud.crud_user.user.get(db=db, id=user_id)
        is_current = False

    if user is None:
        raise UnfoundEntity(message="Пользователь не найден", num=1)

    data, paginator = crud.auth_session.get_page(db=db, page=page, user_id=user.id, is_ended=False)

    return schemas.response.ListOfEntityResponse(
        data=[
            getters.get_auth_session(auth_session=auth_session, user=user if is_current else None)
            for auth_session in data
        ],
        meta=schemas.response.Meta(paginator=paginator)
    )


@router.delete(
    '/cp/users/sessions/{session_id}/',
    tags=["Панель Управления / Пользователи"],
    name="Удалить сеанс пользователя",
    response_model=schemas.response.OkResponse,
    responses=get_responses_description_by_codes([401, 403, 400])
)
def edit_user(
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(in_auth_session(deps.get_current_active_superuser)),
        session_id: int = Path(...),
):
    crud.auth_session.remove_by_id(db=db, id=session_id)

    return schemas.response.OkResponse()
