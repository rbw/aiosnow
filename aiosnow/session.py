from typing import Any

import aiohttp

from aiosnow.request.response import Response


class Session(aiohttp.ClientSession):
    def __init__(self, *args: Any, **kwargs: Any):
        super(Session, self).__init__(
            *args, response_class=kwargs.pop("response_class", Response), **kwargs
        )

    async def request(self, *args, **kwargs) -> Any:  # type: ignore
        return await super().request(*args, **kwargs)
