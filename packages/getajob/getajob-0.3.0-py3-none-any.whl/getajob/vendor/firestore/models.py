from enum import Enum
import typing as t
from pydantic import BaseModel

from getajob.config.settings import SETTINGS


class FirestorePagination(BaseModel):
    start_after: t.Optional[dict] = None
    limit: int = SETTINGS.DEFAULT_PAGE_LIMIT

    class Config:
        arbitrary_types_allowed = True


class FirestoreFilters(BaseModel):
    field: str
    operator: t.Literal[
        "==",
        ">",
        "<",
        ">=",
        "<=",
        "array-contains",
        "in",
        "array-contains-any",
        "not-in",
        "like",  # The like operator is custom soft text
    ]
    value: t.Any


class FirestoreOrderBy(BaseModel):
    field: str
    direction: t.Literal["ASCENDING", "DESCENDING"]


class FirestoreDocument(BaseModel):
    id: str
    data: t.Dict[str, t.Any]


class FirestorePaginatedResponse(BaseModel):
    results: t.List[FirestoreDocument]
    start_after: t.Optional[dict] = None
    count: int = 0

    class Config:
        arbitrary_types_allowed = True


class FirestoreBatchActionType(str, Enum):
    GET = "get"
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"


class FirestoreBatchAction(BaseModel):
    action: FirestoreBatchActionType
    parent_collections: dict
    collection_name: str
    document_data: dict
    document_id: str


class ParentAndCollection(BaseModel):
    parents: dict
    collection: str
    id: str


class JoinAttribute(BaseModel):
    attribute: str
    collection: str
    parent_collections: dict
    data_model: t.Optional[t.Type[BaseModel]] = None


class GetWithJoins(BaseModel):
    parent_collections: dict
    get_id: str
    get_collection: str
    joins: t.List[JoinAttribute]


class QueryWithJoins(BaseModel):
    parent_collections: dict
    collection_name: str
    filters: t.Optional[t.List[FirestoreFilters]] = None
    order_by: t.Optional[FirestoreOrderBy] = None
    pagination: FirestorePagination = FirestorePagination()
    joins: t.List[JoinAttribute]
