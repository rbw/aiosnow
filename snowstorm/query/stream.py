import asyncio
import re

from collections import deque
from urllib.parse import urlencode, parse_qs

import ujson


class Stream:
    exhausted = False

    def __init__(self, session, limit, offset, chunk_size):
        self._connection = session.connection
        self._session = session
        self._limit = limit
        self._offset = offset
        self._chunk_size = chunk_size

    @property
    def _url(self):
        chunk_part = self._offset > self._limit - self._chunk_size
        limit = self._limit if chunk_part else self._chunk_size

        query = urlencode({
            "sysparm_limit": limit,
            "sysparm_offset": self._offset
        })

        return f"{self._session.url}?{query}"

    def _prepare_next(self, links):
        if "next" not in links:
            self.exhausted = True
            return

        url_next = str(links["next"]["url"])
        offset_next = int(parse_qs(url_next).get("sysparm_offset")[0])

        if offset_next >= self._limit:
            self.exhausted = True

        self._offset = offset_next

    async def read(self, **kwargs):
        response = await self._connection.get(self._url, **kwargs)
        items = ujson.loads(await response.text()).get("result")

        yield items

        self._prepare_next(response.links)
