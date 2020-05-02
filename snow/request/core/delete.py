from __future__ import annotations

from typing import TYPE_CHECKING, Any, Tuple

from aiohttp import ClientResponse

from .base import Request

if TYPE_CHECKING:
    from snow import Resource


class DeleteRequest(Request):
    __verb__ = "DELETE"

    def __init__(self, resource: Resource, object_id: str):
        super(DeleteRequest, self).__init__(resource)
        self.object_id = object_id

    async def send(self, *args: Any, **kwargs: Any) -> Tuple[ClientResponse, dict]:
        return await self._send(*args, **kwargs)

    @property
    def url(self) -> str:
        return self.resource.get_url(fragments=[self.object_id])
