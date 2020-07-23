from typing import Any

from . import methods
from .base import BaseRequest


class PostRequest(BaseRequest):
    _method = methods.POST

    def __init__(self, *args: Any, payload: str, **kwargs: Any):
        self.payload = payload
        super(PostRequest, self).__init__(*args, **kwargs)

    def __repr__(self) -> str:
        return self._format_repr(f"payload: {self.payload}")

    async def send(self, *args: Any, **kwargs: Any) -> Any:
        return await self._send(data=self.payload, **kwargs)
