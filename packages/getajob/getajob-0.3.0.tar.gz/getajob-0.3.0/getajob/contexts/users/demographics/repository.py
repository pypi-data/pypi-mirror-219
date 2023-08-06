from getajob.vendor.firestore.repository import FirestoreDB
from getajob.abstractions.repository import (
    SingleChildRepository,
    RepositoryDependencies,
)
from getajob.abstractions.models import Entity, EntityModels

from .models import UserDemographicData, DemographicData


entity_models = EntityModels(
    entity=UserDemographicData,
    create=DemographicData,
    update=DemographicData,
)


class UserDemographicsRepository(SingleChildRepository):
    def __init__(self, db: FirestoreDB):
        super().__init__(
            RepositoryDependencies(db, Entity.USER_DEMOGRAPHICS.value, entity_models),
            required_parent_keys=[Entity.USERS.value],
        )
