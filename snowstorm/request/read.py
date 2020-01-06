from typing import Iterable

from .base import GetRequest
from .stream import PageStream


class Reader:
    def __init__(self, resource, builder):
        self.resource = resource
        self.query = builder.sysparms
        self.schema = resource.schema_cls()

    async def stream(self, *args, **kwargs) -> Iterable:
        stream = PageStream(self.resource, *args, **kwargs, query=self.query)
        while not stream.exhausted:
            async for content in stream.read():
                for item in self.schema.load(content, many=True):
                    yield item

    async def collect(self, *args, **kwargs):
        response = await GetRequest(self.resource, *args, **kwargs).send()
        content = await response.read()
        return self.schema.load(content, many=True)
