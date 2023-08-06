from getajob.vendor.firestore.repository import FirestoreDB
from getajob.abstractions.repository import (
    SingleChildRepository,
    RepositoryDependencies,
)
from getajob.abstractions.models import Entity, EntityModels

from .models import Qualifications, UserQualifications


entity_models = EntityModels(
    entity=UserQualifications,
    create=Qualifications,
    update=Qualifications,
)


class UserQualificationsRepository(SingleChildRepository):
    def __init__(self, db: FirestoreDB):
        super().__init__(
            RepositoryDependencies(db, Entity.USER_QUALIFICATIONS.value, entity_models),
            required_parent_keys=[Entity.USERS.value],
        )
