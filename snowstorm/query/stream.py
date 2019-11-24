from urllib.parse import urlencode, parse_qs

import ujson

from snowstorm.exceptions import StreamExhausted


class Stream:
    exhausted = False

    def __init__(self, session, limit, offset, chunk_size):
        self._connection = session.connection
        self._session = session
        self._limit = limit
        self._offset = offset
        self._chunk_size = chunk_size

    @property
    def _page_size(self):
        if self._limit <= self._chunk_size:
            return self._limit
        elif self._offset + self._chunk_size >= self._limit:
            # Reduce last page to whats requested
            return self._limit - self._offset
        else:
            return self._chunk_size

    @property
    def _url(self):
        query = urlencode({
            "sysparm_limit": self._page_size,
            "sysparm_offset": self._offset
        })

        return f"{self._session.url}?{query}"

    def _prepare_next(self, links):
        if "next" in links:
            url_next = str(links["next"]["url"])
            offset_next = int(parse_qs(url_next).get("sysparm_offset")[0])

            if offset_next >= self._limit:
                raise StreamExhausted
        else:
            raise StreamExhausted

        self._offset = offset_next

    async def read(self, **kwargs):
        response = await self._connection.get(self._url, **kwargs)
        yield ujson.loads(await response.text()).get("result")

        try:
            self._prepare_next(response.links)
        except StreamExhausted:
            self.exhausted = True
