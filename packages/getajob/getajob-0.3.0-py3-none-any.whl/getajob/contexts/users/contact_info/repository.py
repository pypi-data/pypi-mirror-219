from getajob.vendor.firestore.repository import FirestoreDB
from getajob.abstractions.repository import (
    SingleChildRepository,
    RepositoryDependencies,
)
from getajob.abstractions.models import Entity, EntityModels

from .models import (
    UserContactInformation,
    ContactInformation,
)


entity_models = EntityModels(
    entity=UserContactInformation,
    create=ContactInformation,
)


class ContactInformationRepository(SingleChildRepository):
    def __init__(self, db: FirestoreDB):
        super().__init__(
            RepositoryDependencies(
                db, Entity.USER_CONTACT_INFORMATION.value, entity_models
            ),
            required_parent_keys=[Entity.USERS.value],
        )
