import logging

from .base_sender import BaseEmailSender


class FakeEmailSender(BaseEmailSender):

    def send_one(self, subject: str, recipient: str, body: str):
        logging.info(f"Subject: {subject}")
        logging.info(f"Recipient: {recipient}")
        logging.info(f"Body: {body}")
