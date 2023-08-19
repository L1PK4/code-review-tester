
from app import crud, deps, getters, schemas
from app.services.tel_verifier.base_tel_verifier import BaseTelVerifier
from app.utils.response import get_responses_description_by_codes
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

router = APIRouter()


@router.post(
    '/cp/verification-codes/tel/',
    response_model=schemas.response.SingleEntityResponse[
        schemas.tel_verification_code.GettingTelVerificationCode],
    name="Оправить код подтверждения на телефон",
    responses=get_responses_description_by_codes([401, 403, 400, 404]),
    tags=["Вход"]
)
def send_code(
        data: schemas.tel_verification_code.CreatingTelVerificationCode,
        db: Session = Depends(deps.get_db),
        tel_verifier: BaseTelVerifier = Depends(deps.get_tel_verifier)
):

    code_value = tel_verifier.verify(tel=data.tel, code='8085')

    code = crud.crud_tel_verification_code.tel_verification_code.create(
        db=db,
        obj_in=data,
        value=code_value
    )
    return schemas.SingleEntityResponse(
        data=getters.tel_verification_code.get_tel_verification_code(code)
    )  # type: ignore
