from typing import Iterable

import marshmallow

from ..core import GetRequest, StreamLike
from .base import RequestHelper


class Reader(RequestHelper):
    @property
    def schema(self):
        return self.resource.schema_cls(unknown=marshmallow.EXCLUDE)

    async def stream(self, selection, **kwargs) -> Iterable:
        stream = StreamLike(self.resource, query=selection, **kwargs)
        while not stream.exhausted:
            async for content in stream.read():
                for item in self.schema.load(content, many=True):
                    yield item

    async def collect(self, selection, **kwargs) -> dict:
        _, content = await GetRequest(self.resource, query=selection, **kwargs).send()
        return self.schema.load(content, many=True)
