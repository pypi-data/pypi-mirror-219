from getajob.vendor.firestore.repository import FirestoreDB
from getajob.abstractions.repository import (
    SingleChildRepository,
    RepositoryDependencies,
)
from getajob.abstractions.models import Entity, EntityModels

from .models import CreateCompanyDetails, CompanyDetails

entity_models = EntityModels(
    create=CreateCompanyDetails,
    update=CreateCompanyDetails,
    entity=CompanyDetails,
)


class CompanyDetailsRepository(SingleChildRepository):
    def __init__(self, db: FirestoreDB):
        super().__init__(
            RepositoryDependencies(db, Entity.COMPANY_DETAILS.value, entity_models),
            required_parent_keys=[Entity.COMPANIES.value],
        )
