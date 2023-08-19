from app.models.tel_verification_code import TelVerificationCode
from app.schemas.tel_verification_code import GettingTelVerificationCode


def get_tel_verification_code(code: TelVerificationCode) -> GettingTelVerificationCode:
    return GettingTelVerificationCode(
        code=code.value
    )
