from typing import Any

from . import methods
from .base import BaseRequest


class DeleteRequest(BaseRequest):
    _method = methods.DELETE

    def __init__(self, *args: Any, object_id: str, **kwargs: Any):
        self.object_id = object_id
        super(DeleteRequest, self).__init__(*args, **kwargs)
        self.url_segments.append(object_id)

    def __repr__(self) -> str:
        return self._format_repr()

    async def send(self, *args: Any, **kwargs: Any) -> Any:
        kwargs["decode"] = False
        return await self._send(*args, **kwargs)
