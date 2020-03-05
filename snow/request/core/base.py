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

    @property
    def status(self):
        return self.obj.status

    @property
    def links(self):
        return self.obj.links


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

            response = await self._resource.get_cached(item["link"])
            content = await self._get_content(response)
            nested[name] = content

        return nested

    async def _get_content(self, response):
        content_type = response.headers["content-type"]

        if not content_type.startswith(CONTENT_TYPE):
            raise UnexpectedContentType(
                f"Unexpected content-type in response: "
                f"{content_type}, expected: {CONTENT_TYPE}, "
                f"probable causes: instance down or REST API disabled"
            )

        body = await response.text()
        content = ujson.loads(body).get("result")

        if "error" in body:
            err = ErrorSchema().load(content["error"])
            text = f"{err['message']} ({response.status}): {err['detail']}" if err["detail"] else err["message"]
            raise ErrorResponse(text)

        return content

    async def _send(self, **kwargs):
        headers = self.default_headers
        headers.update(kwargs.pop("headers", {}))

        response = await self._session.request(
            self.__verb__,
            kwargs.pop("url", self.url),
            headers={
                **self.default_headers,
                **(headers or {})
            },
            **kwargs
        )

        if response.method == "DELETE" and response.status == 204:
            return dict(result="success")

        content = await self._get_content(response)

        if self._resource.nested_fields:
            for idx, record in enumerate(content):
                nested = await self._resolve_nested(record)
                content[idx].update(nested)

        return content, response
