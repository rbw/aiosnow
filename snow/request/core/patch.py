from __future__ import annotations

from typing import TYPE_CHECKING, Any, Tuple

from aiohttp import ClientResponse

from .base import Request

if TYPE_CHECKING:
    from snow import Resource


class PatchRequest(Request):
    __verb__ = "PATCH"

    def __init__(self, resource: Resource, object_id: str, payload: str):
        super(PatchRequest, self).__init__(resource)
        self.payload = payload
        self.object_id = object_id

    async def send(self, *args: Any, **kwargs: Any) -> Tuple[ClientResponse, dict]:
        return await self.send_resolve(data=self.payload, **kwargs)

    @property
    def url(self) -> str:
        return self.resource.get_url(fragments=[self.object_id])
