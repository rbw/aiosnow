from typing import Union, Any

import aiohttp

from aiosnow.request import Response


class Session(aiohttp.ClientSession):
    async def request(
        self, method: str, url: aiohttp.client.StrOrURL, **kwargs: Any
    ) -> Union[Response, aiohttp.ClientResponse]:
        return await super().request(method, url, **kwargs)
