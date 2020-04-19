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
            response = await self.session.request("GET", url)
            _cache[url] = await response.text()
        else:
            # @TODO: write debug log about cache hit
            pass

        return _cache[url]

    async def __resolve_nested(self, record):
        nested = {}

        for name in self.resource.nested_fields:
            item = record[name]
            if not item or "link" not in item:
                nested[name] = None
                continue

            response = await self.get_cached(item["link"])
            nested[name] = load_content(response)

        return nested

    async def _resolve_nested(self, content):
        if self.resource.nested_fields:
            if isinstance(content, dict):
                nested = await self.__resolve_nested(content)
                content.update(nested)
            elif isinstance(content, list):
                for idx, record in enumerate(content):
                    nested = await self.__resolve_nested(record)
                    content[idx].update(nested)

        return content

    async def send_resolve(self, *args, **kwargs):
        response, content = await self._send(*args, **kwargs)
        return response, await self._resolve_nested(content)

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
