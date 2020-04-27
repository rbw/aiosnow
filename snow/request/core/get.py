from __future__ import annotations

from typing import TYPE_CHECKING, Any, Tuple
from urllib.parse import urlencode

from aiohttp import ClientResponse

from .base import Request

if TYPE_CHECKING:
    from snow import Resource


class GetRequest(Request):
    __verb__ = "GET"

    def __init__(
        self, resource: Resource, limit: int = 10000, offset: int = 0, query: str = None
    ):
        super(GetRequest, self).__init__(resource)
        self.limit = limit
        self.offset = offset
        self.query = query

    async def send(self, *args: Any, **kwargs: Any) -> Tuple[ClientResponse, dict]:
        return await self.send_resolve(**kwargs)

    @property
    def params(self) -> dict:
        return dict(
            sysparm_offset=self.offset,
            sysparm_limit=self.limit,
            sysparm_query=self.query,
        )

    @property
    def url(self) -> str:
        return f"{self.base_url}&{urlencode(self.params)}"
