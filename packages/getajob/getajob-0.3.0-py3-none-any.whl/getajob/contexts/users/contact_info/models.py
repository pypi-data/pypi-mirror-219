import typing as t

from pydantic import BaseModel

from getajob.abstractions.models import BaseDataModel, Location


class ContactInformation(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    phone_number: str | None = None
    show_number_publically: bool = False

    user_location: Location | None = None


class UserContactInformation(ContactInformation, BaseDataModel):
    ...
