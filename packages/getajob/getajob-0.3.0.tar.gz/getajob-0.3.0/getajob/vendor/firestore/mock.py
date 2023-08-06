from mockfirestore import MockFirestore


class MockFirestoreBatchClient:
    def __init__(self, *args, **kwargs):
        ...

    def set(self, *args, **kwargs):
        ...

    def update(self, *args, **kwargs):
        ...

    def delete(self, *args, **kwargs):
        ...

    def commit(self, *args, **kwargs):
        ...


class MockFirestoreClient(MockFirestore):
    def close(self, *args, **kwargs):
        ...

    def batch(self, *args, **kwargs):
        return MockFirestoreBatchClient()
