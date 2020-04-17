from abc import ABC, abstractmethod

import ujson
from aiohttp import ClientSession
from marshmallow import Schema, fields

from snow.consts import CONTENT_TYPE
from snow.exceptions import ErrorResponse, UnexpectedContentType


_cache = {}


class Request(ABC):
    class ErrorSchema(Schema):
        message = fields.String()
        detail = fields.String(allow_none=True)

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

    async def get_result(self, response):
        data = await response.text()
        content = ujson.loads(data)

        if "error" in content:
            err = self.ErrorSchema().load(content["error"])
            text = (
                f"{err['message']} ({response.status}): {err['detail']}"
                if err["detail"]
                else err["message"]
            )
            raise ErrorResponse(text)

        return content["result"]

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

        return response, await self.get_result(response)
