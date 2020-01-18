from urllib.parse import urlencode

from .base import Request


class GetRequest(Request):
    __verb__ = "GET"

    def __init__(self, resource, limit=30, offset=0, query=None):
        super(GetRequest, self).__init__(resource)
        self._limit = limit
        self._offset = offset
        self.query = query

    async def send(self, **kwargs):
        return await self._request(**kwargs)

    @property
    def _page_size(self):
        if not self._limit:
            return False

        return self._limit - self._offset

    @property
    def url(self):
        params = dict(
            sysparm_offset=self._offset,
        )

        if self._page_size:
            params["sysparm_limit"] = self._page_size
        if self.query:
            params["sysparm_query"] = self.query

        return f"{self._resource_url}&{urlencode(params)}"
