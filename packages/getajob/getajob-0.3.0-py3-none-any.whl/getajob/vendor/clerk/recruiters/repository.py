from getajob.vendor.firestore.repository import FirestoreDB
from getajob.abstractions.models import Entity, EntityModels
from getajob.contexts.companies.recruiters.repository import RecruiterRepository


from .models import (
    ClerkCompanyMembershipWebhookEvent,
    ClerkCompanyMembership,
    ClerkCompanyMembershipWebhookType,
    ClerkUpdateCompanyMembership,
    ClerkCompanyMember,
    UpdateClerkCompanyMemberWithRole,
)

entity_models = EntityModels(entity=ClerkCompanyMember)


class WebhookCompanyMembershipRepository:
    def __init__(self, db: FirestoreDB):
        self.repo = RecruiterRepository(db)

    def handle_webhook_event(self, event: ClerkCompanyMembershipWebhookEvent):
        event_dict = {
            ClerkCompanyMembershipWebhookType.organization_membership_created: self.create_recruiter,
            ClerkCompanyMembershipWebhookType.organization_membership_updated: self.update_recruiter,
            ClerkCompanyMembershipWebhookType.organization_membership_deleted: self.delete_recruiter,
        }
        return event_dict[event.type](event)

    def create_recruiter(self, event: ClerkCompanyMembershipWebhookEvent):
        create_event = ClerkCompanyMembership(**event.data)
        recruiter = ClerkCompanyMember(
            **create_event.public_user_data.dict(),
            id=create_event.id,
            role=create_event.role
        )
        return self.repo.create(
            data=recruiter,
            provided_id=create_event.id,
            parent_collections={Entity.COMPANIES.value: create_event.organization.id},
        )

    def delete_recruiter(self, event: ClerkCompanyMembershipWebhookEvent):
        delete_event = ClerkUpdateCompanyMembership(**event.data)
        return self.repo.delete(
            doc_id=delete_event.id,
            parent_collections={Entity.COMPANIES.value: delete_event.organization.id},
        )

    def update_recruiter(self, event: ClerkCompanyMembershipWebhookEvent):
        update_event = ClerkUpdateCompanyMembership(**event.data)
        recruiter = UpdateClerkCompanyMemberWithRole(
            **update_event.public_user_data.dict(), role=update_event.role
        )
        return self.repo.update(
            doc_id=update_event.id,
            data=recruiter,
            parent_collections={Entity.COMPANIES.value: update_event.organization.id},
        )
