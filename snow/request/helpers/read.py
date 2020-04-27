from __future__ import annotations

from typing import TYPE_CHECKING, Any, AsyncGenerator

import marshmallow

from ..core import GetRequest, StreamLike
from .base import RequestHelper

if TYPE_CHECKING:
    from snow.resource import Schema


class Reader(RequestHelper):
    @property
    def schema(self) -> Schema:
        return self.resource.schema_cls(unknown=marshmallow.EXCLUDE)

    async def stream(self, selection: str = None, **kwargs: Any) -> AsyncGenerator:
        stream = StreamLike(self.resource, query=selection, **kwargs)
        while not stream.exhausted:
            async for content in stream.read():
                for item in self.schema.load(content, many=True):
                    yield item

    async def collect(self, selection: str = None, **kwargs: Any) -> list:
        _, content = await GetRequest(self.resource, query=selection, **kwargs).send()
        return self.schema.load(content, many=True)
