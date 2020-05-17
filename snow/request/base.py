from __future__ import annotations

import logging
import time
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Dict, Tuple
from urllib.parse import urlencode, urlparse

from aiohttp import client_exceptions

from snow.consts import CONTENT_TYPE
from snow.exceptions import ClientConnectionError, UnexpectedContentType

from .response import Response

if TYPE_CHECKING:
    from snow import Resource


_cache: dict = {}


class Request(ABC):
    session: Any
    log = logging.getLogger("snow.request")

    def __init__(self, resource: Resource):
        self.resource = resource
        self.schema = resource.schema
        self.session = resource.session
        self.headers_default = {"Content-type": CONTENT_TYPE}
        self.base_url = resource.get_url()

    @abstractmethod
    def __repr__(self) -> str:
        pass

    @property
    @abstractmethod
    def url(self) -> str:
        pass

    @abstractmethod
    async def send(self, *args: Any, **kwargs: Any) -> Tuple[Response, dict]:
        pass

    @property
    @abstractmethod
    def _method(self) -> str:
        pass

    def _format_repr(self, params: str = "") -> str:
        return f"<{self.__class__.__name__} {urlparse(self.url).path} [{params}]>"

    @property
    def _request_id(self) -> str:
        return hex(id(self))

    async def get_cached(self, url: str) -> dict:
        if url not in _cache:
            record_id = urlparse(url).path.split("/")[-1]

            response = await self._send(
                method="GET", url=url, resolve=False, transform=False
            )
            self.log.debug(f"Caching response for: {record_id}")
            _cache[url] = response.data

        return _cache[url]

    async def _get_joined(self, content: dict) -> dict:
        if not self.resource.nested_fields:
            pass
        elif isinstance(content, dict):
            nested = await self._resolve_nested(content)
            content.update(nested)
        elif isinstance(content, list):
            for idx, record in enumerate(content):
                nested = await self._resolve_nested(record)
                content[idx].update(nested)

        return content

    async def _resolve_nested(self, content: dict) -> dict:
        nested: Dict[Any, Any] = {}

        for field_name in self.resource.nested_fields:
            item = content[field_name]
            if not item or "link" not in item:
                nested[field_name] = None
                continue

            params = dict(
                sysparm_fields=",".join(
                    getattr(self.schema, field_name).nested.__dict__.keys()
                ),
            )

            nested[field_name] = await self.get_cached(
                f"{item['link']}?{urlencode(params)}"
            )

        return nested

    async def _send(
        self,
        headers_extra: dict = None,
        decode: bool = True,
        transform: bool = True,
        resolve: bool = True,
        **kwargs: Any,
    ) -> Response:
        headers = self.headers_default
        headers.update(**headers_extra or {})
        kwargs["headers"] = headers

        method = kwargs.pop("method", self._method)
        url = kwargs.pop("url", self.url)

        try:
            req_id = hex(int(round(time.time() * 1000)))
            self.log.debug(f"REQ_{req_id}: {self}")
            response = await self.session.request(method, url, **kwargs)
            self.log.debug(f"REQ_{req_id}: {response}")

            if not decode:
                response.data = await response.read()
                return response
            elif not response.content_type.startswith(CONTENT_TYPE):
                raise UnexpectedContentType(
                    f"Unexpected content-type in response: "
                    f"{response.content_type}, expected: {CONTENT_TYPE}, "
                    f"probable causes: instance down or REST API disabled"
                )

            await response.load()
            content = response.data

            if resolve:
                content = await self._get_joined(content)

        except client_exceptions.ClientConnectionError as exc:
            raise ClientConnectionError(str(exc)) from exc

        if transform:
            response.data = self.schema.load(content, many=isinstance(content, list))

        return response
