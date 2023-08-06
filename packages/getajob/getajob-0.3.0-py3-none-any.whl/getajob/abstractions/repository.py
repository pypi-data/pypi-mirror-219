import typing as t
from datetime import datetime
from functools import wraps

from pydantic import BaseModel

from getajob.utils import generate_random_short_code
from getajob.exceptions import (
    KafkaEventTopicNotProvidedError,
    EntityNotFound,
    MissingParentKeyError,
)
from getajob.vendor.firestore.models import (
    FirestoreDocument,
    FirestorePagination,
    FirestoreFilters,
    FirestoreOrderBy,
    FirestorePaginatedResponse,
    FirestoreBatchAction,
    FirestoreBatchActionType,
    JoinAttribute,
    GetWithJoins,
    QueryWithJoins,
)
from getajob.vendor.firestore.repository import FirestoreDB
from getajob.vendor.kafka.models import (
    KafkaEventType,
    BaseKafkaMessage,
)
from .models import (
    PaginatedResponse,
    BaseDataModel,
    RepositoryDependencies,
)


def format_to_schema(
    document: FirestoreDocument, entity_model: t.Type[BaseModel]
) -> BaseModel:
    id_included_dict = {
        "id": document.id,
        **document.data,
    }
    return entity_model(**id_included_dict)


def format_paginated_response(
    res: FirestorePaginatedResponse, entity_model: t.Optional[t.Type[BaseModel]] = None
):
    if entity_model is None:
        data = [
            {
                "id": doc.id,
                **doc.data,
            }
            for doc in res.results
        ]
    else:
        data = [format_to_schema(doc, entity_model) for doc in res.results]  # type: ignore
    return PaginatedResponse(data=data, next=res.start_after)  # type: ignore


def ensure_parent_keys(method):
    """
    This decorator ensures that the parent_collections parameter is provided
    when querying a sub-collection.
    """

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        if not self.required_parent_keys:
            return method(self, *args, **kwargs)
        kwarg_parent_collections = kwargs.get("parent_collections", {})
        potential_arg_parent_collections = [
            arg for arg in args if isinstance(arg, dict)
        ]
        for key in self.required_parent_keys:
            if key not in kwarg_parent_collections and not any(
                key in arg for arg in potential_arg_parent_collections
            ):
                raise MissingParentKeyError(f"Missing parent key: {key}")
        return method(self, *args, **kwargs)

    return wrapper


def query_collection(
    db: FirestoreDB,
    collection_name: str,
    parent_collections: dict = {},
    entity_model: t.Optional[t.Type[BaseModel]] = None,
    filters: t.Optional[t.List[FirestoreFilters]] = None,
    order_by: t.Optional[FirestoreOrderBy] = None,
    pagination: FirestorePagination = FirestorePagination(),
):
    """
    This query method is kept outside of the base repository to allow for it to be used
    with any collection name. Otherwise, you would have to instantiantiate a repository
    to perform a query which confines broader queries across multiple collections.
    """
    res = db.query(
        parent_collections=parent_collections,
        collection_name=collection_name,
        filters=filters,
        order_by=order_by,
        pagination=pagination,
    )
    return format_paginated_response(res, entity_model)


class BaseRepository:
    """
    This is the base repository layer that sites between a context's repository and the database.
    It's purpose is to provide basic query function with a conversion to pydantic models.

    It also handles the relationship between collections and sub-collections and can
    be given a Kafka client and configuration to create event streams based on CRUD operations.

    A Collection is a root level document in firestore, such as a company or a user.
    A Sub-Collection is a document that is a child of a root level document, such as a company's recruiters.

    The parent_collections parameter is a dictionary of the parent collections and their ids.
    For example, if you are querying a company's recruiters, the parent_collections would be:
    {
        "companies": "company_id"
    }

    The required_parent_keys parameter is a list of the keys that must be in the parent_collections
    dictionary. This is used to ensure that the parent_collections are provided when querying a sub-collection.

    This class should not be used directly, but should be extended by the
    parent, multiple children, and single child repositories defined below.

    These 3 repository classes are then meant to be used by the context layer of the application.

    """

    def __init__(
        self,
        dependencies: RepositoryDependencies,
        required_parent_keys: t.Optional[t.List[str]] = None,
    ):
        self.db = dependencies.db
        self.collection_name = dependencies.collection_name
        self.entity_models = dependencies.entity_models
        self.kafka = dependencies.kafka
        self.kafka_event_config = dependencies.kafka_event_config
        self.required_parent_keys = required_parent_keys

        # If kafka client given but with no configuration, complain about it
        if self.kafka and not self.kafka_event_config:
            raise KafkaEventTopicNotProvidedError()

    def _produce_repository_kafka_event(
        self, event_type: KafkaEventType, object_id: str, data: dict | None = None
    ):
        if (
            not self.kafka
            or not self.kafka_event_config
            or not self.kafka_event_config.dict()[event_type]
        ):
            return
        self.kafka.publish(
            topic=self.kafka_event_config.topic,
            message=BaseKafkaMessage(
                message_type=f"{event_type.value}_{self.collection_name}",
                object_id=object_id,
                data=data if data else None,
            ),
        )

    @ensure_parent_keys
    def get(
        self,
        doc_id: str,
        parent_collections: dict = {},
        internal_get_request: bool = False,
    ) -> BaseModel:
        res = self.db.get(parent_collections, self.collection_name, doc_id)
        if not internal_get_request:
            self._produce_repository_kafka_event(KafkaEventType.get, doc_id)
        return format_to_schema(res, self.entity_models.entity)

    @ensure_parent_keys
    def get_with_filters(
        self,
        doc_id: str,
        filters: t.List[FirestoreFilters],
        parent_collections: dict = {},
    ) -> BaseModel:
        res = self.db.get_with_filters(
            parent_collections, self.collection_name, doc_id, filters
        )
        return format_to_schema(res, self.entity_models.entity)

    @ensure_parent_keys
    def create(
        self,
        data: BaseModel,
        parent_collections: dict = {},
        provided_id: t.Optional[str] = None,
    ) -> BaseModel:
        data_dict = data.dict()
        data_dict.update(
            {
                "created": datetime.now(),
                "updated": datetime.now(),
            }
        )
        document_id = provided_id or generate_random_short_code()
        res = self.db.create(
            parent_collections=parent_collections,
            collection_name=self.collection_name,
            document_id=document_id,
            document_data=data_dict,
        )
        self._produce_repository_kafka_event(KafkaEventType.create, res.id, data.dict())
        return format_to_schema(res, self.entity_models.entity)

    @ensure_parent_keys
    def update(
        self,
        doc_id: str,
        data: BaseModel,
        parent_collections: dict = {},
    ) -> BaseModel:
        original_item = self.get(doc_id, parent_collections, True).dict()
        for key, val in data.dict().items():
            if val is not None:
                original_item[key] = val
        original_item["updated"] = datetime.now()
        res = self.db.update(
            parent_collections, self.collection_name, doc_id, original_item
        )
        self._produce_repository_kafka_event(
            KafkaEventType.update, doc_id, original_item
        )
        return format_to_schema(res, self.entity_models.entity)

    @ensure_parent_keys
    def delete(
        self,
        doc_id: str,
        parent_collections: dict = {},
    ) -> bool:
        deleted_object = self.get(doc_id, parent_collections, True)
        self._produce_repository_kafka_event(
            KafkaEventType.delete, doc_id, deleted_object.dict()
        )
        return self.db.delete(parent_collections, self.collection_name, doc_id)

    @ensure_parent_keys
    def get_one_by_attribute(
        self,
        attribute: str,
        value: t.Any,
        parent_collections: dict = {},
    ) -> t.Union[BaseModel, None]:
        res = self.db.get_one_by_attribute(
            parent_collections, self.collection_name, attribute, value
        )
        return format_to_schema(res, self.entity_models.entity)

    @ensure_parent_keys
    def query(
        self,
        parent_collections: dict = {},
        filters: t.Optional[t.List[FirestoreFilters]] = None,
        order_by: t.Optional[FirestoreOrderBy] = None,
        pagination: FirestorePagination = FirestorePagination(),
    ) -> PaginatedResponse:
        return query_collection(
            db=self.db,
            collection_name=self.collection_name,
            entity_model=self.entity_models.entity,
            parent_collections=parent_collections,
            filters=filters,
            order_by=order_by,
            pagination=pagination,
        )

    @ensure_parent_keys
    def batch_action(
        self,
        data: t.List[BaseDataModel | BaseModel],
        action: FirestoreBatchActionType,
        parent_collections: dict = {},
    ):
        batch_action = [
            FirestoreBatchAction(
                action=action,
                parent_collections=parent_collections,
                collection_name=self.collection_name,
                document_data=item.dict(),
                document_id=item.id  # type: ignore
                if action != FirestoreBatchActionType.CREATE
                else generate_random_short_code(),
            )
            for item in data
        ]
        return self.db.batch_action(batch_action)

    @ensure_parent_keys
    def batch_create(
        self,
        data: t.List[BaseModel],
        parent_collections: dict = {},
    ):
        return self.batch_action(
            data, FirestoreBatchActionType.CREATE, parent_collections
        )

    @ensure_parent_keys
    def batch_update(
        self,
        data: t.List[BaseDataModel],
        parent_collections: dict = {},
    ):
        return self.batch_action(data, FirestoreBatchActionType.UPDATE, parent_collections)  # type: ignore

    @ensure_parent_keys
    def batch_delete(
        self,
        data: t.List[BaseDataModel],
        parent_collections: dict = {},
    ):
        return self.batch_action(data, FirestoreBatchActionType.DELETE, parent_collections)  # type: ignore

    @ensure_parent_keys
    def get_with_joins(
        self,
        doc_id: str,
        parent_collections: dict = {},
        joins: t.List[JoinAttribute] = [],
    ) -> dict:
        """
        TODO - the repo layer is supposed to always return pydantic models
        The current models don't support joins so we need to figure out how to do this

        For now, these will just return the dictionary results
        """
        res = self.db.get_with_joins(
            join_model=GetWithJoins(
                parent_collections=parent_collections,
                get_id=doc_id,
                get_collection=self.collection_name,
                joins=joins,
            )
        )
        return res.data

    @ensure_parent_keys
    def query_with_joins(
        self,
        parent_collections: dict = {},
        filters: t.Optional[t.List[FirestoreFilters]] = None,
        order_by: t.Optional[FirestoreOrderBy] = None,
        pagination: FirestorePagination = FirestorePagination(),
        joins: t.List[JoinAttribute] = [],
    ):
        res = self.db.query_with_joins(
            join_query=QueryWithJoins(
                parent_collections=parent_collections,
                collection_name=self.collection_name,
                filters=filters,
                order_by=order_by,
                pagination=pagination,
                joins=joins,
            )
        )
        return format_paginated_response(res, None)


class ParentRepository(BaseRepository):
    """
    This class extends the base repository and is meant for
    interacting with root level documents.

    An example is a company, this is a root level object
    """

    def __init__(
        self,
        dependencies: RepositoryDependencies,
    ):
        super().__init__(dependencies)


class MultipleChildrenRepository(BaseRepository):
    """
    This class extends the base repository is meant for interacting with a
    sub-collection of a root level document where there can be many
    sub collections of the same type.

    An example is a company's recruiters, which there may be many of directly under the company
    """

    def __init__(
        self, dependencies: RepositoryDependencies, required_parent_keys: t.List[str]
    ):
        super().__init__(dependencies)
        self.required_parent_keys = required_parent_keys


class SingleChildRepository:
    """
    This class extends the base repository is meant for interacting with a
    sub-collection of a root level document where there can be only one sub
    collection of the same type.

    An example is a company's details, which there can only be one of
    directly under the company
    """

    def __init__(
        self, dependencies: RepositoryDependencies, required_parent_keys: t.List[str]
    ):
        self.dependencies = dependencies
        self.repo = BaseRepository(dependencies)
        self.required_parent_keys = required_parent_keys

    @ensure_parent_keys
    def get_sub_entity(self, parent_collections: dict):
        return self.repo.get(self.dependencies.collection_name, parent_collections)

    @ensure_parent_keys
    def set_sub_entity(self, data: BaseModel, parent_collections: dict):
        try:
            return self.repo.update(
                self.dependencies.collection_name, data, parent_collections
            )
        except EntityNotFound:
            return self.repo.create(
                data, parent_collections, self.dependencies.collection_name
            )
