from abc import ABC, abstractmethod

from aiohttp import ClientSession

from snow.consts import CONTENT_TYPE
from snow.exceptions import UnexpectedContentType

from .response import load_content

_cache = {}


class Request(ABC):
    session: ClientSession

    def __init__(self, resource):
        self.resource = resource
        self.session = resource.session
        self.headers_default = {"Content-type": CONTENT_TYPE}
        self.base_url = resource.get_url()

    @property
    @abstractmethod
    def url(self):
        pass

    @abstractmethod
    async def send(self, *args, **kwargs):
        pass

    @property
    @abstractmethod
    def __verb__(self):
        pass

    async def get_cached(self, url):
        if url not in _cache:
            _cache[url] = await self.session.request("GET", url)
        else:
            # @TODO: write debug log about cache hit
            pass

        return _cache[url]

    async def _send(self, headers_extra: dict = None, **kwargs):
        headers = self.headers_default
        headers.update(**headers_extra or {})
        kwargs["headers"] = headers

        response = await self.session.request(
            self.__verb__, kwargs.pop("url", self.url), **kwargs
        )

        if response.status == 204:
            return response, {}

        content_type = response.headers["content-type"]
        if not content_type.startswith(CONTENT_TYPE):
            raise UnexpectedContentType(
                f"Unexpected content-type in response: "
                f"{content_type}, expected: {CONTENT_TYPE}, "
                f"probable causes: instance down or REST API disabled"
            )

        content = await response.text()
        return response, load_content(content)
