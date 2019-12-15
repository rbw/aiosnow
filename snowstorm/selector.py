from .stream import Stream
from typing import Iterable


class Selector:
    def __init__(self, resource, query):
        self.query = query
        self.resource = resource
        self.schema = resource.schema_cls()

    async def all(self, limit=30, offset=0, chunk_size=8) -> Iterable:
        stream = Stream(self.resource, limit, offset, chunk_size)
        while not stream.exhausted:
            async for content in stream.read():
                print(content)
                for item in self.schema.load(content, many=True):
                    yield item
