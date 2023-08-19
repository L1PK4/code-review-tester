import logging
import urllib
from typing import List

import requests

from .base_sender import BaseEmailSender


class TelegramEmailSender(BaseEmailSender):

    def __init__(self, bot_token: str, recipients: List[str]):
        self.bot_token = bot_token
        self.recipients = recipients

    def send_one(self, subject: str, recipient: str, body: str):

        text = f"Subject: {subject}\nRecipient: {recipient}\nBody:\n {body}"

        query = {
            "text": text,
            "disable_web_page_preview": 'True'
        }

        for tg_recipient in self.recipients:
            query["chat_id"] = tg_recipient

            response = requests.get(f"https://api.telegram.org/bot{self.bot_token}/sendMessage?{urllib.parse.urlencode(query)}")
            logging.info(response.text)
