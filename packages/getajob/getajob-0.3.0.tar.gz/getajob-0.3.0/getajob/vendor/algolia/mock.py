from algoliasearch.search_client import SearchClient, SearchIndex
from .models import AlgoliaSearchResults


class MockAlgoliaIndex(SearchIndex):
    # pylint: disable=super-init-not-called
    def __init__(self, *args, **kwargs):
        ...

    def search(self, *args, **kwargs):
        return AlgoliaSearchResults(
            hits=[],
            nbHits=0,
            page=0,
            nbPages=0,
            hitsPerPage=0,
            processingTimeMS=0,
            exhaustiveNbHits=False,
            query="",
            params="",
        ).dict()

    def get_object(self, *args, **kwargs):
        ...


class MockAlgoliaClient(SearchClient):
    # pylint: disable=super-init-not-called
    def __init__(self, *args, **kwargs):
        ...

    def init_index(self, *args, **kwargs):
        return MockAlgoliaIndex()
