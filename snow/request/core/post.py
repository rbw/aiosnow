from __future__ import annotations

from typing import TYPE_CHECKING, Any, Tuple

from aiohttp import ClientResponse

from .base import Request

if TYPE_CHECKING:
    from snow import Resource


class PostRequest(Request):
    __verb__ = "POST"

    def __init__(self, resource: Resource, payload: str):
        super(PostRequest, self).__init__(resource)
        self.payload = payload

    async def send(self, *args: Any, **kwargs: Any) -> Tuple[ClientResponse, dict]:
        return await self.send_resolve(data=self.payload, **kwargs)

    @property
    def url(self) -> str:
        return self.base_url
