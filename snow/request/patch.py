from typing import Any

from . import methods
from .base import BaseRequest


class PatchRequest(BaseRequest):
    _method = methods.PATCH

    def __init__(self, object_id: str, payload: str, *args: Any, **kwargs: Any):
        self.payload = payload
        self.object_id = object_id
        self.url_segments.append(object_id)
        super(PatchRequest, self).__init__(*args, **kwargs)

    def __repr__(self) -> str:
        return self._format_repr(
            f"object_id: {self.object_id}, payload: {self.payload}"
        )

    async def send(self, *args: Any, **kwargs: Any) -> Any:
        return await self._send(data=self.payload, **kwargs)
