import typing as t
from enum import Enum

from pydantic import BaseModel

from getajob.abstractions.models import BaseDataModel


class RaceEnum(str, Enum):
    WHITE = "White or Caucasian"
    INDIGENOUS = "American Indian or Alaska Native"
    MIDDLE_EASTERN = "Middle Eastern"
    BLACK = "Black"
    ASIAN = "Asian"
    HISPANIC = "Hispanic or Latino"
    PREFER_NOT_TO_SAY = "Prefer not to say"
    OTHER = "Other"


class GenderEnum(str, Enum):
    MALE = "Male"
    FEMALE = "Female"
    NON_BINARY = "Non-binary"
    PREFER_NOT_TO_SAY = "Prefer not to say"
    OTHER = "Other"


class DemographicData(BaseModel):
    birth_year: int | None = None
    race: RaceEnum | None = None
    gender: GenderEnum | None = None
    has_disibility: bool | None = None
    arrest_record: bool | None = None

    consent_to_use_data: bool | None = None


class UserDemographicData(DemographicData, BaseDataModel):
    ...
