from algoliasearch.search_client import SearchClient

from .client_factory import AlgoliaClientFactory
from .models import AlgoliaIndex, AlgoliaSearchParams, AlgoliaSearchResults


class AlgoliaSearchRepository:
    def __init__(self, client: SearchClient = AlgoliaClientFactory().get_client()):  # type: ignore
        self.client = client

    def search(self, index_name: AlgoliaIndex, query: AlgoliaSearchParams):
        search_params = {
            "query": query.query,
            "page": query.page,
            "hitsPerPage": query.hits_per_page,
        }
        if query.filters:
            search_params["filters"] = query.filters
        if query.facet_filters:
            search_params["facetFilters"] = query.facet_filters
        if query.attributes_to_retrieve:
            search_params["attributesToRetrieve"] = query.attributes_to_retrieve
        index = self.client.init_index(index_name.value)
        res = index.search(query.query, search_params)
        return AlgoliaSearchResults(**res)

    def get_object(self, index_name: AlgoliaIndex, object_id: str):
        index = self.client.init_index(index_name.value)
        return index.get_object(object_id)
