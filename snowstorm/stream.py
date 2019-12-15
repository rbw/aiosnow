from urllib.parse import urlencode, parse_qs

import ujson

from snowstorm.exceptions import StreamExhausted, ErrorResponse
from snowstorm.schemas import SnowErrorText


class Stream:
    exhausted = False

    def __init__(self, resource, limit, offset, chunk_size):
        self._connection = resource.connection
        self._resource = resource
        self._limit = limit
        self._offset = offset
        self._chunk_size = chunk_size
        self._fields = None
        self._url_start = resource.get_url()

    @property
    def _page_size(self):
        if self._offset + self._chunk_size >= self._limit:
            return self._limit - self._offset

        return self._chunk_size

    @property
    def _url(self):
        params = dict(
            sysparm_limit=self._page_size,
            sysparm_offset=self._offset,
        )

        return f"{self._url_start}&{urlencode(params)}"

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
        content = ujson.loads(await response.text())

        if "error" in content:
            err = SnowErrorText().load(content["error"])
            text = f"{err['message'] ({err['detail']})}" if err["detail"] else err["message"]
            raise ErrorResponse(text)

        yield content.get("result")

        try:
            self._prepare_next(response.links)
        except StreamExhausted:
            self.exhausted = True
