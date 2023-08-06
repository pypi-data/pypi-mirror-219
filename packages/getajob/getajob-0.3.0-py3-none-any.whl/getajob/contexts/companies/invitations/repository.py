from getajob.vendor.firestore.repository import FirestoreDB
from getajob.abstractions.repository import (
    MultipleChildrenRepository,
    RepositoryDependencies,
)
from getajob.abstractions.models import Entity, EntityModels

from .models import RecruiterInvitation

entity_models = EntityModels(entity=RecruiterInvitation)


class RecruiterInvitationsRepository(MultipleChildrenRepository):
    def __init__(self, db: FirestoreDB):
        super().__init__(
            RepositoryDependencies(
                db, Entity.RECRUITER_INVITATIONS.value, entity_models
            ),
            required_parent_keys=[Entity.COMPANIES.value],
        )
