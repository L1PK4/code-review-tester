from app.models.email_verification_code import EmailVerificationCode
from app.schemas.email_verification_code import GettingEmailVerificationCode


def get_email_verification_code(code: EmailVerificationCode) -> GettingEmailVerificationCode:
    return GettingEmailVerificationCode(
        code=code.value
    )
