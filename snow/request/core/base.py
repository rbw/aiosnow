from abc import ABC, abstractmethod

from aiohttp import ClientSession, client_exceptions, http_exceptions, web_exceptions
from marshmallow import EXCLUDE, Schema, fields

from snow.consts import CONTENT_TYPE
from snow.exceptions import (
    ClientConnectionError,
    RequestError,
    ServerError,
    UnexpectedContentType,
)


class ErrorSchema(Schema):
    message = fields.String()
    detail = fields.String(allow_none=True)


class ContentSchema(Schema):
    error = fields.Nested(ErrorSchema)
    result = fields.Raw()
    status = fields.String(missing=None)


async def _process_response(data, status):
    if not isinstance(data, dict):
        return

    content = ContentSchema(unknown=EXCLUDE, many=False).load(data)

    if "error" in content:
        err = content["error"]
        msg = f"{err['message']}: {err['detail']}" if err["detail"] else err["message"]

        raise RequestError(msg, status)

    return content["result"]


async def process_response(response):
    data = await response.json()
    processed = await _process_response(data, response.status)

    try:
        response.raise_for_status()
    except (
        client_exceptions.ClientResponseError,
        http_exceptions.HttpProcessingError,
    ) as exc:
        raise ServerError(exc.message, exc.status) from exc
    except web_exceptions.HTTPException as exc:
        raise ServerError(exc.text, exc.status) from exc

    return processed


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
            _, _cache[url] = await self._send(method="GET", url=url)
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

            nested[name] = await self.get_cached(item["link"])

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

        try:
            response = await self.session.request(
                kwargs.pop("method", self.__verb__),
                kwargs.pop("url", self.url),
                **kwargs,
            )
        except client_exceptions.ClientConnectionError as exc:
            raise ClientConnectionError(str(exc)) from exc

        if response.status == 204:
            return response, {}

        content_type = response.headers["content-type"]
        if not content_type.startswith(CONTENT_TYPE):
            raise UnexpectedContentType(
                f"Unexpected content-type in response: "
                f"{content_type}, expected: {CONTENT_TYPE}, "
                f"probable causes: instance down or REST API disabled"
            )

        return response, await process_response(response)
