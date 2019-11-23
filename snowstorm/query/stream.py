import asyncio

import ijson
import ujson

from ijson.common import ObjectBuilder
from urllib.parse import urlencode, parse_qs

from .parser import StreamParser


class Stream:
    def __init__(self, session, limit, offset):
        self._connection = session.connection
        self._session = session
        self._limit = limit or 0
        self._offset = offset or 0

    @property
    def url(self):
        query = urlencode({
            "sysparm_limit": self._limit,
            "sysparm_offset": self._offset
        })

        return f"{self._session.url}?{query}"

    async def read(self, **kwargs):
        response = await self._connection.get(self.url, **kwargs)
        # group_url_next = str(responses[-1].links["next"]["url"])
        # next_url = int(parse_qs(group_url_next).get("sysparm_offset")[0])

        test = StreamParser.parse(response.content)
        yield test

        # yield ujson.loads(await response.text()).get("result")
