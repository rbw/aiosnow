from urllib.parse import urlencode

from .base import Request


class GetRequest(Request):
    __verb__ = "GET"

    def __init__(self, resource, limit=30, offset=0, query=None):
        super(GetRequest, self).__init__(resource)
        self._limit = limit
        self._offset = offset
        self.query = query

    async def _resolve_nested(self, record):
        nested = {}

        for name in self.resource.nested_fields:
            item = record[name]
            if not item or "link" not in item:
                nested[name] = None
                continue

            response = await self.get_cached(item["link"])
            nested[name] = await self.get_result(response)

        return nested

    async def send(self, **kwargs):
        return await self._send(**kwargs)

    @property
    def _page_size(self):
        if not self._limit:
            return False

        return self._limit - self._offset

    @property
    def url(self):
        params = dict(sysparm_offset=self._offset)

        if self._page_size:
            params["sysparm_limit"] = self._page_size
        if self.query:
            params["sysparm_query"] = self.query

        return f"{self.base_url}&{urlencode(params)}"
