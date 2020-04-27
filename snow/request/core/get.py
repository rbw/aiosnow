from urllib.parse import urlencode

from .base import Request


class GetRequest(Request):
    __verb__ = "GET"

    def __init__(self, resource, limit: int = 10000, offset: int = 0, query: dict = None):
        super(GetRequest, self).__init__(resource)
        self.limit = limit
        self.offset = offset
        self.query = query

    async def send(self, **kwargs):
        return await self.send_resolve(**kwargs)

    @property
    def params(self):
        return dict(
            sysparm_offset=self.offset,
            sysparm_limit=self.limit,
            sysparm_query=self.query
        )

    @property
    def url(self):
        return f"{self.base_url}&{urlencode(self.params)}"
