from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from getajob.config.settings import SETTINGS

from .client_factory import SendGridClientFactory


class SendGridRepository:
    def __init__(self, sendgrid_client: SendGridAPIClient = SendGridClientFactory.get_client()):  # type: ignore
        self.sendgrid_client = sendgrid_client

    def send_email(self, to_address: str, subject: str, html_content: str):
        message = Mail(
            from_email=SETTINGS.SENDGRID_FROM_EMAIL,
            to_emails=to_address,
            subject=subject,
            html_content=html_content,
        )
        return self.sendgrid_client.send(message)
