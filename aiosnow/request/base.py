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
        self, api_url: str, session: Session, fields: dict = None,
    ):
        self.api_url = api_url
        self.session = session
        self.fields = fields or {}
        self.url_segments: List[str] = []
        self.headers_default = {"Content-type": CONTENT_TYPE}
        self._req_id = f"REQ_{hex(int(round(time.time() * 1000)))}"

    @property
    def url_params(self) -> dict:
        params = dict(sysparm_display_value="all")
        if self.fields:
            params["sysparm_fields"] = ",".join(self.fields)

        return params

    @property
    def url(self) -> str:
        api_url = self.api_url

        if self.url_segments:
            # Append path segments
            api_url += "/" + "/".join(map(str, self.url_segments))

        return f"{api_url}?{urlencode(self.url_params)}"

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

    async def _send(
        self, headers_extra: dict = None, decode: bool = True, **kwargs: Any,
    ) -> Response:
        headers = self.headers_default
        headers.update(**headers_extra or {})
        kwargs["headers"] = headers

        method = kwargs.pop("method", self._method)

        try:
            self.log.debug(f"{self._req_id}: {self}")
            response = await self.session.request(method, self.url, **kwargs)
            self.log.debug(f"{self._req_id}: {response}")
        except client_exceptions.ClientConnectionError as exc:
            raise ClientConnectionError(str(exc)) from exc

        if method == methods.DELETE and response.status == 204:
            return response

        if not response.content_type.startswith(CONTENT_TYPE):
            raise UnexpectedContentType(
                f"Unexpected content-type in response: "
                f"{response.content_type}, expected: {CONTENT_TYPE}, "
                f"probable causes: instance down or REST API disabled"
            )

        if decode:
            await response.load_document()
        else:
            response.data = await response.read()

        return response
