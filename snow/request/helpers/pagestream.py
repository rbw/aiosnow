from __future__ import annotations

from typing import Any, AsyncGenerator
from urllib.parse import parse_qs

from multidict import MultiDictProxy

from snow.exceptions import StreamExhausted
from snow.request import GetRequest


class Pagestream(GetRequest):
    exhausted = False

    def __init__(self, *args: Any, chunk_size: int = 500, **kwargs: Any):
        super(Pagestream, self).__init__(*args, **kwargs)
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

    async def next(self, **kwargs: Any) -> AsyncGenerator:
        response = await self._send(**kwargs)

        try:
            self._prepare_next(response.links)
        except StreamExhausted:
            self.exhausted = True

        yield response
