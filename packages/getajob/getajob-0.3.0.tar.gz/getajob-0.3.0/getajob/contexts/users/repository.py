from getajob.vendor.firestore.repository import FirestoreDB
from getajob.abstractions.repository import ParentRepository, RepositoryDependencies
from getajob.abstractions.models import Entity, EntityModels
from .models import User


entity_models = EntityModels(entity=User)


class UserRepository(ParentRepository):
    def __init__(
        self,
        db: FirestoreDB,
    ):
        super().__init__(RepositoryDependencies(db, Entity.USERS.value, entity_models))

    def get_user(self, id: str):
        return super().get(id)

    def get_by_email(self, email: str):
        return self.get_one_by_attribute("email", email)
