from __future__ import annotations

import logging
import time
from abc import ABC, abstractmethod
from typing import Any, List, Tuple
from urllib.parse import urlencode, urlparse

from aiohttp import client_exceptions

from aiosnow.consts import CONTENT_TYPE
from aiosnow.exceptions import ClientConnectionError, UnexpectedContentType
from aiosnow.request import methods
from aiosnow.session import Session

from .response import Response


class BaseRequest(ABC):
    session: Session
    log = logging.getLogger("aiosnow.request")

    def __init__(
        self,
        api_url: str,
        session: Session,
        fields: dict = None,
        headers: dict = None,
        params: dict = None,
        resolve: bool = False,
    ):
        self.api_url = api_url
        self.session = session
        self.fields = fields or {}
        self.url_segments: List[str] = []
        self._resolve = resolve
        self._default_headers = {"Content-type": CONTENT_TYPE, **(headers or {})}
        self._default_params = params or {}
        self._req_id = f"REQ_{hex(int(round(time.time() * 1000)))}"

    @property
    def params(self) -> dict:
        params = dict(sysparm_display_value="all")
        if self.fields:
            params["sysparm_fields"] = ",".join(self.fields)

        return {**params, **self._default_params}

    @property
    def url(self) -> str:
        api_url = self.api_url

        if self.url_segments:
            # Append path segments
            api_url += "/" + "/".join(map(str, self.url_segments))

        return f"{api_url}?{urlencode(self.params)}"

    @abstractmethod
    def __repr__(self) -> str:
        pass

    @abstractmethod
    async def send(self, *args: Any, **kwargs: Any) -> Tuple[Response, dict]:
        pass

    @property
    @abstractmethod
    def _method(self) -> str:
        pass

    @property
    def _request_id(self) -> str:
        return hex(id(self))

    def _format_repr(self, params: str = "") -> str:
        return f"<{self.__class__.__name__} {urlparse(self.url).path} [{params}]>"

    async def _send(self, headers_extra: dict = None, **kwargs: Any,) -> Response:
        headers = self._default_headers
        headers.update(**headers_extra or {})
        kwargs["headers"] = headers

        method = kwargs.pop("method", self._method)
        decode = kwargs.pop("decode", True)

        try:
            self.log.debug(f"{self._req_id}: {self}")
            response = await self.session.request(method, self.url, **kwargs)
            self.log.debug(f"{self._req_id}: {response}")
        except client_exceptions.ClientConnectionError as exc:
            raise ClientConnectionError(str(exc)) from exc

        if method == methods.DELETE and response.status == 204:
            return response

        if not decode:
            response.data = await response.read()
        elif not response.content_type.startswith(CONTENT_TYPE):
            raise UnexpectedContentType(
                f"Unexpected content-type in response: "
                f"{response.content_type}, expected: {CONTENT_TYPE}, "
                f"probable causes: instance down or REST API disabled"
            )
        else:
            await response.load_document()

        return response
