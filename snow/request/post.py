from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .base import Request

if TYPE_CHECKING:
    from snow import Resource


class PostRequest(Request):
    _method = "POST"

    def __init__(self, resource: Resource, payload: str):
        self.payload = payload
        super(PostRequest, self).__init__(resource)

    def __repr__(self) -> str:
        return self._format_repr(f"payload: {self.payload}")

    async def send(self, *args: Any, **kwargs: Any) -> Any:
        return await self._send(data=self.payload, **kwargs)

    @property
    def url(self) -> str:
        return self.base_url
