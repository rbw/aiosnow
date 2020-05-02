from __future__ import annotations

from typing import TYPE_CHECKING, Any, AsyncGenerator
from urllib.parse import parse_qs

import marshmallow
from multidict import MultiDictProxy

from snow.exceptions import StreamExhausted

from ..core import GetRequest
from .base import RequestHelper

if TYPE_CHECKING:
    from snow.resource import Schema


class PageStream(GetRequest):
    exhausted = False

    def __init__(self, *args: Any, chunk_size: int = 500, **kwargs: Any):
        super(PageStream, self).__init__(*args, **kwargs)
        self._chunk_size = chunk_size
        self._fields = None

    @property
    def _page_size(self) -> int:
        if self._offset + self._chunk_size >= self.limit:
            return self.limit - self._offset

        return self._chunk_size

    def _prepare_next(self, links: MultiDictProxy) -> None:
        if "next" in links:
            url_next = str(links["next"]["url"])
            query = parse_qs(url_next)  # type: Any
            offset_next = int(query.get("sysparm_offset")[0])

            if offset_next >= self.limit:
                raise StreamExhausted
        else:
            raise StreamExhausted

        self._offset = offset_next

    async def read(self, **kwargs: Any) -> AsyncGenerator:
        response, content = await self.send_resolve(**kwargs)

        try:
            self._prepare_next(response.links)
        except StreamExhausted:
            self.exhausted = True

        yield content


class Reader(RequestHelper):
    @property
    def schema(self) -> Schema:
        return self.resource.schema_cls(unknown=marshmallow.EXCLUDE)

    async def stream(self, selection: str = None, **kwargs: Any) -> AsyncGenerator:
        stream = PageStream(self.resource, query=selection, **kwargs)
        while not stream.exhausted:
            async for content in stream.read():
                for item in self.schema.load(content, many=True):
                    yield item

    async def collect(self, selection: str = None, **kwargs: Any) -> list:
        _, content = await GetRequest(self.resource, query=selection, **kwargs).send()
        return self.schema.load(content, many=True)
