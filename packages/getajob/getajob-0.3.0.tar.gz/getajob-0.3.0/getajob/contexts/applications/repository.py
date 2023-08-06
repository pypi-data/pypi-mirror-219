import typing as t

from getajob.abstractions.models import Entity
from getajob.abstractions.repository import ParentRepository, RepositoryDependencies
from getajob.vendor.firestore.models import FirestoreFilters
from getajob.vendor.firestore.repository import FirestoreDB
from getajob.vendor.kafka.repository import KafkaProducerRepository
from getajob.vendor.kafka.models import KafkaEventConfig, KafkaTopic
from getajob.contexts.users.resumes.repository import ResumeRepository
from getajob.contexts.companies.jobs.repository import JobsRepository

from .models import entity_models, UserCreatedApplication
from .unit_of_work import ApplicationsUnitOfWork


class ApplicationRepository(ParentRepository):
    def __init__(
        self, db: FirestoreDB, kafka: t.Optional[KafkaProducerRepository] = None
    ):
        kafka_event_config = KafkaEventConfig(
            topic=KafkaTopic.applications,
            create=True,
            update=True,
            delete=True,
            get=True,
        )
        super().__init__(
            RepositoryDependencies(
                db, Entity.APPLICATIONS.value, entity_models, kafka, kafka_event_config
            ),
        )

    def user_creates_application(
        self, user_id: str, application: UserCreatedApplication
    ):
        return ApplicationsUnitOfWork(self).user_creates_application(
            user_id=user_id,
            resume_repo=ResumeRepository(self.db),
            job_repo=JobsRepository(self.db),
            create_application=application,
        )

    def get_applications_by_job(self, company_id: str, job_id: str):
        return super().query(
            filters=[
                FirestoreFilters(field="company_id", operator="==", value=company_id),
                FirestoreFilters(field="job_id", operator="==", value=job_id),
            ],
        )

    def get_application_by_job_and_application_id(
        self, company_id: str, job_id: str, job_application_id: str
    ):
        return super().get_with_filters(
            doc_id=job_application_id,
            filters=[
                FirestoreFilters(field="company_id", operator="==", value=company_id),
                FirestoreFilters(field="job_id", operator="==", value=job_id),
            ],
        )

    def get_applications_by_user(self, user_id):
        return super().query(
            filters=[
                FirestoreFilters(
                    field="user_id",
                    operator="==",
                    value=user_id,
                )
            ],
        )

    def get_application_by_user_id_and_application_id(
        self, user_id: str, job_application_id: str
    ):
        return super().get_with_filters(
            doc_id=job_application_id,
            filters=[
                FirestoreFilters(
                    field="user_id",
                    operator="==",
                    value=user_id,
                )
            ],
        )
