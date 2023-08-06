from getajob.vendor.firestore.repository import FirestoreDB
from getajob.abstractions.repository import (
    SingleChildRepository,
    RepositoryDependencies,
)
from getajob.abstractions.models import Entity, EntityModels

from .models import UserJobPreferences, JobPreferences


entity_models = EntityModels(
    entity=UserJobPreferences,
    create=JobPreferences,
    update=JobPreferences,
)


class UserJobPreferencesRepository(SingleChildRepository):
    def __init__(self, db: FirestoreDB):
        super().__init__(
            RepositoryDependencies(
                db, Entity.USER_JOB_PREFERENCES.value, entity_models
            ),
            required_parent_keys=[Entity.USERS.value],
        )
