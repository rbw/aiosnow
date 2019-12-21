from .stream import PageStream
from typing import Iterable


class Selector:
    def __init__(self, resource, query):
        self.query = query
        self.resource = resource
        self.schema = resource.schema_cls()

    async def all(self, *args, **kwargs) -> Iterable:
        stream = PageStream(self.resource, *args, **kwargs)
        while not stream.exhausted:
            async for content in stream.read():
                for item in self.schema.load(content, many=True):
                    yield item

    async def update(self, payload):
        print(self.query)
        print(payload)
