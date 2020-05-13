from __future__ import annotations

from typing import TYPE_CHECKING, Any
from urllib.parse import urlencode

from .base import Request

if TYPE_CHECKING:
    from snow import Resource


class GetRequest(Request):
    __method__ = "GET"

    def __init__(
        self, resource: Resource, limit: int = 10000, offset: int = 0, query: str = None
    ):
        self.limit = limit
        self.offset = offset
        self.query = query
        super(GetRequest, self).__init__(resource)

    def __repr__(self) -> str:
        params = f"query: {self.query}, limit: {self.limit}, offset: {self.offset}"
        return self._format_repr(params)

    async def send(self, *args: Any, **kwargs: Any) -> Any:
        return await self._send(**kwargs)

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
