from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .base import Request

if TYPE_CHECKING:
    from snow import Resource


class PatchRequest(Request):
    __method__ = "PATCH"

    def __init__(self, resource: Resource, object_id: str, payload: str):
        self.payload = payload
        self.object_id = object_id
        super(PatchRequest, self).__init__(resource)

    def __repr__(self) -> str:
        return self._format_repr(
            f"object_id: {self.object_id}, payload: {self.payload}"
        )

    async def send(self, *args: Any, **kwargs: Any) -> Any:
        return await self._send(data=self.payload, **kwargs)

    @property
    def url(self) -> str:
        return self.resource.get_url(fragments=[self.object_id])
