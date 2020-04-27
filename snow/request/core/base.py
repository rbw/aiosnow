from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Dict, Tuple

from aiohttp import (
    ClientResponse,
    ClientSession,
    client_exceptions,
    http_exceptions,
    web_exceptions,
)
from marshmallow import EXCLUDE, Schema, fields

from snow.consts import CONTENT_TYPE
from snow.exceptions import (
    ClientConnectionError,
    RequestError,
    ServerError,
    UnexpectedContentType,
    UnexpectedResponseContent,
)

if TYPE_CHECKING:
    from snow import Resource


class ErrorSchema(Schema):
    """Defines the structure of the ServiceNow error response content"""

    message = fields.String()
    detail = fields.String(allow_none=True)


class ContentSchema(Schema):
    """Defines structure of the ServiceNow response content"""

    error = fields.Nested(ErrorSchema)
    result = fields.Raw()
    status = fields.String(missing=None)


async def process_response(response: ClientResponse) -> dict:
    data = await response.json()

    if isinstance(data, dict):
        content = ContentSchema(unknown=EXCLUDE, many=False).load(data)

        # Was there an error?
        if "error" in content:
            err = content["error"]
            msg = (
                f"{err['message']}: {err['detail']}"
                if err["detail"]
                else err["message"]
            )

            raise RequestError(msg, response.status)

        content = content["result"]
    else:
        try:
            # Something went wrong, most likely out of the ServiceNow application's control:
            # Raise exception if we got a HTTP error status back.
            response.raise_for_status()
        except (
            client_exceptions.ClientResponseError,
            http_exceptions.HttpProcessingError,
        ) as exc:
            raise ServerError(exc.message, exc.code) from exc
        except web_exceptions.HTTPException as exc:
            raise ServerError(exc.text or "", exc.status) from exc
        else:
            # Non-JSON content along with a HTTP 200 returned: Unexpected.
            text = await response.text()
            raise UnexpectedResponseContent(
                f"Unexpected response received from server: {text}", 200
            )

    return content


_cache = {}


class Request(ABC):
    session: ClientSession

    def __init__(self, resource: Resource):
        self.resource = resource
        self.session = resource.session
        self.headers_default = {"Content-type": CONTENT_TYPE}
        self.base_url = resource.get_url()

    @property
    @abstractmethod
    def url(self) -> str:
        pass

    @abstractmethod
    async def send(self, *args: Any, **kwargs: Any) -> Tuple[ClientResponse, dict]:
        pass

    @property
    @abstractmethod
    def __verb__(self) -> str:
        pass

    async def get_cached(self, url: str) -> dict:
        if url not in _cache:
            _, _cache[url] = await self._send(method="GET", url=url)
        else:
            # @TODO: write debug log about cache hit
            pass

        return _cache[url]

    async def __resolve_nested(self, record: dict) -> dict:
        nested: Dict[Any, Any] = {}

        for name in self.resource.nested_fields:
            item = record[name]
            if not item or "link" not in item:
                nested[name] = None
                continue

            nested[name] = await self.get_cached(item["link"])

        return nested

    async def _resolve_nested(self, content: dict) -> dict:
        if self.resource.nested_fields:
            if isinstance(content, dict):
                nested = await self.__resolve_nested(content)
                content.update(nested)
            elif isinstance(content, list):
                for idx, record in enumerate(content):
                    nested = await self.__resolve_nested(record)
                    content[idx].update(nested)

        return content

    async def send_resolve(
        self, *args: Any, **kwargs: Any
    ) -> Tuple[ClientResponse, dict]:
        response, content = await self._send(*args, **kwargs)
        return response, await self._resolve_nested(content)

    async def _send(
        self, headers_extra: dict = None, **kwargs: Any
    ) -> Tuple[ClientResponse, dict]:
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
