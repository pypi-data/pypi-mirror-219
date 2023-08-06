from getajob.vendor.firestore.repository import FirestoreDB
from getajob.abstractions.repository import (
    SingleChildRepository,
    RepositoryDependencies,
)
from getajob.abstractions.models import Entity, EntityModels

from .models import CoverLetter, CreateCoverLetter, UpdateCoverLetter

entity_models = EntityModels(
    entity=CoverLetter,
    create=CreateCoverLetter,
    update=UpdateCoverLetter,
)


class CoverLetterRepository(SingleChildRepository):
    def __init__(self, db: FirestoreDB):
        super().__init__(
            RepositoryDependencies(db, Entity.COVER_LETTERS.value, entity_models),
            required_parent_keys=[Entity.USERS.value],
        )
