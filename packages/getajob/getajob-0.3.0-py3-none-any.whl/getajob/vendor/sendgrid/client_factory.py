from sendgrid import SendGridAPIClient
from getajob.abstractions.vendor_client_factory import VendorClientFactory
from getajob.config.settings import SETTINGS

from .mock import MockSendGrid


class SendGridClientFactory(VendorClientFactory):
    @staticmethod
    def _return_mock():
        return MockSendGrid()

    @staticmethod
    def _return_client():
        return SendGridAPIClient(SETTINGS.SENDGRID_API_KEY)
