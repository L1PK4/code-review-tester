from typing import Any
import uuid
from app.services.payment.base_payment import BasePayment
from app.utils.logging import lprint


class FakePayment(BasePayment):
    def make_payment(self, amount: int, **kwargs) -> dict[str, Any]:
        lprint(
            f"FakePayment.make_payment: amount: {amount};\nkwargs: {kwargs}"
        )
        return {
            'order_num': uuid.uuid4().hex,
            'pay_link': 'https://axas.ru',
        }
