from getajob.vendor.firestore.repository import FirestoreDB
from getajob.abstractions.repository import ParentRepository, RepositoryDependencies
from getajob.abstractions.models import Entity, EntityModels

from .models import Company

entity_models = EntityModels(entity=Company)


class CompanyRepository(ParentRepository):
    def __init__(self, db: FirestoreDB):
        super().__init__(
            RepositoryDependencies(db, Entity.COMPANIES.value, entity_models)
        )
