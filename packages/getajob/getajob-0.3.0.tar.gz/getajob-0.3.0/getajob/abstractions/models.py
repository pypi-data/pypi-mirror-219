import typing as t
from enum import Enum
from datetime import datetime
from dataclasses import dataclass

from pydantic import BaseModel

from getajob.config.settings import SETTINGS
from getajob.vendor.firestore.repository import FirestoreDB
from getajob.vendor.kafka.repository import KafkaProducerRepository
from getajob.vendor.kafka.models import KafkaEventConfig


DataSchema = t.Type[BaseModel]


@dataclass
class PaginatedRequest:
    last: str = None  # type: ignore
    limit: int = SETTINGS.DEFAULT_PAGE_LIMIT


@dataclass
class PaginatedResponse:
    next: t.Optional[dict]
    data: list[DataSchema] | list[dict[str, t.Any]]


@dataclass
class EntityModels:
    entity: DataSchema
    create: t.Optional[DataSchema] = None
    update: t.Optional[DataSchema] = None


class BaseDataModel(BaseModel):
    id: str
    created: datetime
    updated: datetime


@dataclass
class MethodsToInclude:
    get_all: bool = True
    get_by_id: bool = True
    create: bool = True
    update: bool = True
    delete: bool = True


class Entity(str, Enum):
    USERS = "users"  # Comes from clerk
    USER_DETAILS = "user_details"  # What we add to user data
    ADMIN_USERS = "admin_users"
    SKILLS = "skills"
    COVER_LETTERS = "cover_letters"
    RESUMES = "resumes"
    COMPANIES = "companies"  # Comes from clerk
    COMPANY_DETAILS = "company_details"  # What we add to company data
    RECRUITERS = "recruiters"  # Comes from clerk
    RECRUITER_INVITATIONS = "recruiter_invitations"  # Comes from clerk
    RECRUITER_DETAILS = "recruiter_details"  # What we add to recruiter data
    JOBS = "jobs"
    APPLICATIONS = "applications"
    USER_NOTIFICATIONS = "user_notifications"
    SCHEDULED_EVENTS = "scheduled_events"

    # Child collections
    USER_CONTACT_INFORMATION = "user_contact_information"
    USER_DEMOGRAPHICS = "user_demographics"
    USER_JOB_PREFERENCES = "user_job_preferences"
    USER_QUALIFICATIONS = "user_qualifications"


class Location(BaseModel):
    address_line_1: str
    address_line_2: str | None = None
    city: str
    state: str
    zipcode: str
    country: str
    lat: float
    lon: float


@dataclass
class RepositoryDependencies:
    db: FirestoreDB
    collection_name: str
    entity_models: EntityModels
    kafka: t.Optional[KafkaProducerRepository] = None
    kafka_event_config: t.Optional[KafkaEventConfig] = None
