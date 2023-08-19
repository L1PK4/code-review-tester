
from app import crud, deps, getters, schemas
from app.services.email_sender.smtp_sender import SmtpEmailSender
from app.utils.response import get_responses_description_by_codes
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

router = APIRouter()


@router.post(
    '/cp/verification-codes/email/',
    response_model=schemas.response.SingleEntityResponse[
        schemas.email_verification_code.GettingEmailVerificationCode],
    name="Оправить код подтверждения на email",
    responses=get_responses_description_by_codes([401, 403, 400, 404]),
    tags=["Вход"]
)
def send_code(
        data: schemas.email_verification_code.CreatingEmailVerificationCode,
        db: Session = Depends(deps.get_db),
        email_sender: SmtpEmailSender = Depends(deps.get_email_sender)
):
    code = crud.crud_email_verification_code.email_verification_code.create(
        db=db, obj_in=data)
    email_sender.send_one(
        "Email confirmation",
        data.email,
        f"<h1>Here is your code: {code.value}</h1>"
    )
    return schemas.SingleEntityResponse(
        data=getters.email_verification_code.get_email_verification_code(code)
    )  # type: ignore
