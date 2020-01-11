from typing import Iterable

from ..core import GetRequest

from .stream import PageStream


class Reader:
    def __init__(self, resource):
        self.resource = resource
        self.schema = resource.schema_cls()

    async def stream(self, *args, **kwargs) -> Iterable:
        stream = PageStream(self.resource, *args, **kwargs)
        while not stream.exhausted:
            async for content in stream.read():
                for item in self.schema.load(content, many=True):
                    yield item

    async def collect(self, *args, **kwargs) -> dict:
        response = await GetRequest(self.resource, *args, **kwargs).send()
        content = await response.read()
        return self.schema.load(content, many=True)
