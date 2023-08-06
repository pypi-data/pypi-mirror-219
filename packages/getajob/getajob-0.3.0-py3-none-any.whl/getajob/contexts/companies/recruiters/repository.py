from getajob.vendor.firestore.repository import FirestoreDB
from getajob.abstractions.repository import (
    MultipleChildrenRepository,
    RepositoryDependencies,
)
from getajob.abstractions.models import Entity, EntityModels

from .models import Recruiter

entity_models = EntityModels(entity=Recruiter)


class RecruiterRepository(MultipleChildrenRepository):
    def __init__(self, db: FirestoreDB):
        super().__init__(
            RepositoryDependencies(db, Entity.RECRUITERS.value, entity_models),
            required_parent_keys=[Entity.COMPANIES.value],
        )
