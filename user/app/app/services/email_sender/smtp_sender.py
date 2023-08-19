import logging

import emails
from app.config import settings
from app.utils.logging import lprint

from .base_sender import BaseEmailSender


class SmtpEmailSender(BaseEmailSender):

    def send_one(self, subject: str, recipient: str, body: str):
        message = emails.Message(
            subject=subject,
            html=body,
            mail_from=(
                settings.EMAILS_FROM_NAME,
                settings.EMAILS_FROM_EMAIL
            ),
        )
        smtp_options = {
            "host": settings.SMTP_HOST,
            "port": settings.SMTP_PORT
        }
        if settings.SMTP_TLS:
            smtp_options["ssl"] = True
        if settings.SMTP_USER:
            smtp_options["user"] = settings.SMTP_USER
        if settings.SMTP_PASSWORD:
            smtp_options["password"] = settings.SMTP_PASSWORD
        # lprint(
        #     f"Sending email to {recipient} with subject {subject} and options {smtp_options}")
        response = message.send(to=recipient, smtp=smtp_options)

        lprint(f"send email result: {response}")
