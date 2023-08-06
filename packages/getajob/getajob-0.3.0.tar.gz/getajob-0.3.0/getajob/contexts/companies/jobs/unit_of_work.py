from getajob.abstractions.repository import BaseRepository
from getajob.abstractions.models import Entity

from .models import CreateJob


class JobsUnitOfWork:
    def __init__(self, job_repo: BaseRepository):
        self.repo = job_repo

    def create_job(self, company_id: str, data: CreateJob):
        # Other business logic here
        return self.repo.create(
            data, parent_collections={Entity.COMPANIES.value: company_id}
        )
