from urllib.parse import parse_qs

from snow.exceptions import StreamExhausted

from ..core import GetRequest


class StreamLike(GetRequest):
    exhausted = False

    def __init__(self, *args, chunk_size=500, **kwargs):
        super(StreamLike, self).__init__(*args, **kwargs)
        self._chunk_size = chunk_size
        self._fields = None

    @property
    def _page_size(self):
        if self._offset + self._chunk_size >= self._limit:
            return self._limit - self._offset

        return self._chunk_size

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
        response = await self.send(**kwargs)

        try:
            self._prepare_next(response.links)
        except StreamExhausted:
            self.exhausted = True

        yield await response.read()
