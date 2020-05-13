from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .base import Request

if TYPE_CHECKING:
    from snow import Resource


class DeleteRequest(Request):
    __method__ = "DELETE"

    def __init__(self, resource: Resource, object_id: str):
        self.object_id = object_id
        super(DeleteRequest, self).__init__(resource)

    def __repr__(self) -> str:
        return self._format_repr()

    async def send(self, *args: Any, **kwargs: Any) -> Any:
        # kwargs["decode"] = False
        return await self._send(*args, decode=False, **kwargs)

    @property
    def url(self) -> str:
        return self.resource.get_url(fragments=[self.object_id])
