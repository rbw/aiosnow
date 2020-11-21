from typing import Any

from aiosnow.utils import convert_size

from . import methods
from .base import BaseRequest


class PostRequest(BaseRequest):
    _method = methods.POST

    def __init__(self, *args: Any, payload: str, **kwargs: Any):
        self.payload = payload
        super(PostRequest, self).__init__(*args, **kwargs)

    def __repr__(self) -> str:
        if isinstance(self.payload, bytes):
            size, unit = convert_size(len(self.payload))
            return self._format_repr(f"size: {size} {unit}")

        return self._format_repr(f"payload: {self.payload}")

    async def send(self, *args: Any, **kwargs: Any) -> Any:
        return await self._send(data=self.payload, **kwargs)
