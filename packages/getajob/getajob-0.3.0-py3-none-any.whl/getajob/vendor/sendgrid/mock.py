from sendgrid import SendGridAPIClient


class MockSendGrid(SendGridAPIClient):
    # pylint: disable=super-init-not-called
    def __init__(self, *args, **kwargs):
        ...

    def send(self, *args, **kwargs):
        ...
