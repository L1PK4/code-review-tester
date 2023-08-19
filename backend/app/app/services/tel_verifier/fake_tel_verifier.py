from abc import ABC, abstractmethod

from app.services.tel_verifier.base_tel_verifier import BaseTelVerifier
from app.utils.code import fake_gen


class FakeTelVerifier(BaseTelVerifier):

    def verify(self, tel: str, code: str | None = None) -> str:
        if code is None:
            return fake_gen(n=4)
        else:
            return code
