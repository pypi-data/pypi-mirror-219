import typing as t
from fastapi import HTTPException

from getajob.abstractions.models import Entity
from getajob.abstractions.repository import BaseRepository
from getajob.contexts.companies.jobs.models import Job
from getajob.vendor.firestore.models import FirestoreFilters

from .models import UserCreatedApplication, CreateApplication


class ApplicationsUnitOfWork:
    def __init__(self, application_repo: BaseRepository):
        self.application_repo = application_repo

    def user_creates_application(
        self,
        user_id: str,
        resume_repo: BaseRepository,
        job_repo: BaseRepository,
        create_application: UserCreatedApplication,
    ):
        # Check that the company and job is still viable
        job = t.cast(
            Job,
            job_repo.get(
                create_application.job_id,
                parent_collections={
                    Entity.COMPANIES.value: create_application.company_id
                },
            ),
        )
        if job.position_filled:
            raise HTTPException(status_code=400, detail="Job has been filled")

        # Check that user hasn't already applied to this job
        user_application = self.application_repo.query(
            filters=[
                FirestoreFilters(field="user_id", operator="==", value=user_id),
                FirestoreFilters(
                    field="job_id", operator="==", value=create_application.job_id
                ),
            ]
        )
        if user_application.data:
            raise HTTPException(
                status_code=400, detail="You have already applied to this job"
            )

        # Check that resume exists
        assert resume_repo.get(
            parent_collections={Entity.USERS.value: user_id},
            doc_id=create_application.resume_id,
        )

        # Create the application
        return self.application_repo.create(
            data=CreateApplication(
                user_id=user_id,
                job_id=create_application.job_id,
                resume_id=create_application.resume_id,
                company_id=create_application.company_id,
            )
        )
