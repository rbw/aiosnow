from abc import ABC, abstractmethod

import ujson

from marshmallow import Schema, fields
from aiohttp import ClientSession
from snow.consts import CONTENT_TYPE
from snow.exceptions import UnexpectedContentType, ErrorResponse


class ErrorSchema(Schema):
    message = fields.String()
    detail = fields.String(allow_none=True)


class Response:
    def __init__(self, obj):
        self.obj = obj

    def __getattr__(self, item):
        return getattr(self.obj, item)

    async def get_content(self):
        content_type = self.headers["content-type"]

        if not content_type.startswith(CONTENT_TYPE):
            raise UnexpectedContentType(
                f"Unexpected content-type in response: "
                f"{content_type}, expected: {CONTENT_TYPE}, "
                f"probable causes: instance down or REST API disabled"
            )

        body = await self.text()
        content = ujson.loads(body)

        if "error" in content:
            err = ErrorSchema().load(content["error"])
            text = f"{err['message']} ({self.status}): {err['detail']}" if err["detail"] else err["message"]
            raise ErrorResponse(text)

        return content["result"]


class Request(ABC):
    _session: ClientSession

    def __init__(self, resource):
        self._session = resource.session
        self._resource = resource
        self._resource_url = resource.get_url()
        self.default_headers = {
            "Content-type": CONTENT_TYPE
        }

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

    async def _resolve_nested(self, record):
        nested = {}

        for name in self._resource.nested_fields:
            item = record[name]
            if not item or "link" not in item:
                nested[name] = None
                continue

            response = Response(await self._resource.get_cached(item["link"]))
            nested[name] = await response.get_content()

        return nested

    async def _send(self, **kwargs):
        headers = self.default_headers
        headers.update(kwargs.pop("headers", {}))

        response = Response(
            await self._session.request(
                self.__verb__,
                kwargs.pop("url", self.url),
                headers={
                    **self.default_headers,
                    **(headers or {})
                },
                **kwargs
            )
        )

        if response.status == 204:
            return response, {}

        content = await response.get_content()

        if self._resource.nested_fields:
            if isinstance(content, dict):
                nested = await self._resolve_nested(content)
                content.update(nested)
            elif isinstance(content, list):
                for idx, record in enumerate(content):
                    nested = await self._resolve_nested(record)
                    content[idx].update(nested)

        return response, content
