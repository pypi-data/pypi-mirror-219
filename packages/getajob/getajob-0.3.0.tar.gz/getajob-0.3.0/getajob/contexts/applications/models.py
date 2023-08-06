import typing as t
from enum import Enum

from pydantic import BaseModel

from getajob.abstractions.models import EntityModels, BaseDataModel


class ApplicationStatus(str, Enum):
    draft = "draft"
    submitted = "submitted"
    accepted = "accepted"
    rejected = "rejected"
    withdrawn = "withdrawn"


class UserCreatedApplication(BaseModel):
    company_id: str
    job_id: str
    resume_id: str
    cover_letter_content: t.Optional[str] = None


class CreateApplication(UserCreatedApplication):
    user_id: str
    application_status: ApplicationStatus = ApplicationStatus.submitted


class UpdateApplication(BaseModel):
    application_status: ApplicationStatus | None = None


class Application(CreateApplication, BaseDataModel):
    ...


entity_models = EntityModels(
    entity=Application,
    create=CreateApplication,
    update=UpdateApplication,
)
