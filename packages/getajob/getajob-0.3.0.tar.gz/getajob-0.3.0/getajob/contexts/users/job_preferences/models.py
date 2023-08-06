import typing as t
from enum import Enum

from pydantic import BaseModel

from getajob.abstractions.models import BaseDataModel


class JobTypeEnum(str, Enum):
    FULL_TIME = "Full-time"
    PART_TIME = "Part-time"
    CONTRACT = "Contract"
    TEMPORARY = "Temporary"
    INTERNSHIP = "Internship"
    VOLUNTEER = "Volunteer"


class JobSchedule(BaseModel):
    # TODO enums e'rywhere baby
    days: t.List[str]
    shifts: t.List[str]
    schedules: t.List[str]


class PayEnum(str, Enum):
    HOURLY = "Hourly"
    WEEKLY = "Weekly"
    BI_WEEKLY = "Bi-weekly"
    MONTHLY = "Monthly"
    ANNUALLY = "Annually"


class WorkSettingEnum(str, Enum):
    REMOTE = "Remote"
    IN_PERSON = "In-person"
    HYBRID = "Hybrid"
    TEMPORARILY_REMOTE = "Temporarily Remote"


class IndustryEnum(str, Enum):
    TECHNOLOGY = "Technology"
    FINANCE = "Finance"
    HEALTHCARE = "Healthcare"
    EDUCATION = "Education"
    GOVERNMENT = "Government"
    RETAIL = "Retail"
    HOSPITALITY = "Hospitality"
    CONSTRUCTION = "Construction"
    MANUFACTURING = "Manufacturing"


class DesiredPay(BaseModel):
    minimum_pay: int
    pay_period: PayEnum


class JobPreferences(BaseModel):
    desired_job_title: str | None = None
    desired_job_types: JobTypeEnum | None = None
    desired_schedule: JobSchedule | None = None
    desired_pay: DesiredPay | None = None
    willing_to_relocate: bool | None = None
    desired_work_settings: t.List[WorkSettingEnum]
    desired_industries: t.List[IndustryEnum]
    ready_to_start_immediately: bool | None = None


class UserJobPreferences(JobPreferences, BaseDataModel):
    ...
