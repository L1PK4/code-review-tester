import uuid
from typing import Any
from urllib.parse import urlencode
import requests

from app.services.payment.base_payment import BasePayment


class SberPayment(BasePayment):
    def __init__(
            self,
            user_name: str,
            password: str,
            base_url: str,
    ) -> None:
        self.user_name = user_name
        self.password = password
        self.base_url = base_url
        super().__init__()

    def make_payment(self, amount: int, **kwargs) -> dict[str, Any]:
        order_num = uuid.uuid4().hex
        params = {
            'amount': amount,
            'orderNumber': order_num,
            'userName': self.user_name,
            'password': self.password,
            **kwargs
        }

        total_url = self.base_url + '?' + urlencode(params)
        response = requests.request("GET", total_url, verify=False)
        return {
            'order_num': order_num,
            'pay_link': response.json().get('formUrl'),
        }
