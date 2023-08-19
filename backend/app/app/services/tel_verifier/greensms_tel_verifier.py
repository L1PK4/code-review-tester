from abc import ABC, abstractmethod

import requests

from app.exceptions import UnprocessableEntity
from app.services.tel_verifier.base_tel_verifier import BaseTelVerifier
from app.utils.code import fake_gen


class GreensmsTelVerifier(BaseTelVerifier):

    def __init__(self, user: str, password: str):
        self.user = user
        self.password = password

    def verify(self, tel: str, code: str | None = None) -> str:
        url = "https://api3.greensms.ru/call/send"

        payload = f'to={tel}&user={self.user}&pass={self.password}'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        try:
            response = requests.request("POST", url, headers=headers, data=payload).json()
            code_value = response['code']
            if len(code_value) != 4 or code_value[0] == '-':
                raise UnprocessableEntity(message='Что-то пошло не так', num=1)
            return code_value
        except:
            raise UnprocessableEntity(message='Что-то пошло не так', num=2)
