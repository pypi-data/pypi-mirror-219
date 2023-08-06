from getajob.vendor.firestore.repository import FirestoreDB
from getajob.abstractions.repository import (
    MultipleChildrenRepository,
    RepositoryDependencies,
)
from getajob.abstractions.models import Entity, EntityModels

from .models import Resume, CreateResume


entity_models = EntityModels(
    entity=Resume,
    create=CreateResume,
    update=CreateResume,
)


class ResumeRepository(MultipleChildrenRepository):
    def __init__(self, db: FirestoreDB):
        super().__init__(
            RepositoryDependencies(db, Entity.RESUMES.value, entity_models),
            required_parent_keys=[Entity.USERS.value],
        )
