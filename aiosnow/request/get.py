from __future__ import annotations

from typing import Any, Dict, Union
from urllib.parse import urlparse

from . import methods
from .base import BaseRequest

_cache: dict = {}


class GetRequest(BaseRequest):
    _method = methods.GET

    def __init__(
        self,
        *args: Any,
        nested_fields: dict = None,
        limit: int = 10000,
        offset: int = 0,
        query: str = None,
        **kwargs: Any,
    ):
        self.nested_fields = list(self._nested_with_path(nested_fields or {}, []))
        self._limit = offset + limit
        self._offset = offset
        self.query = query
        super(GetRequest, self).__init__(*args, **kwargs)

    def __repr__(self) -> str:
        params = (
            f"query: {self.query or None}, limit: {self.limit}, offset: {self.offset}"
        )
        return self._format_repr(params)

    @property
    def offset(self) -> int:
        return self._offset

    @property
    def limit(self) -> int:
        return self._limit

    def _nested_with_path(self, fields, path_base):
        path = path_base or []

        for k, v in fields.items():
            if not hasattr(v, "nested"):
                continue

            yield path + [k], k, v.schema
            yield from list(self._nested_with_path(v.schema.fields, path_base=path + [k]))

    def _get_expanded(self, path, document, nested_data, level=1):
        waypoint = path[level - 1]

        if waypoint not in document:
            document[waypoint] = {}

        if level < len(path):
            return self._get_expanded(path, document, nested_data, level+1)
        elif level == len(path):
            document[waypoint] = nested_data

        return document

    async def __expand_nested(self, document: dict):
        for path, field_name, _ in self.nested_fields:
            data = document.get(field_name)
            if data and "link" in data:
                document[field_name] = self._get_expanded(path, document, await self.get_cached(data["link"]))

        return document

    async def _expand_nested(
        self, content: Union[dict, list, None]
    ) -> Union[dict, list, None]:
        if not self.nested_fields:
            pass
        elif isinstance(content, dict):
            content = await self.__expand_nested(content)
        elif isinstance(content, list):
            for idx, record in enumerate(content):
                content[idx] = await self.__expand_nested(record)

        return content

    async def get_cached(self, url: str) -> dict:
        if url not in _cache:
            record_id = urlparse(url).path.split("/")[-1]
            request = GetRequest(url, self.session)
            response = await request._send(method=methods.GET)
            self.log.debug(f"Caching response for: {record_id}")
            _cache[url] = response.data

        return _cache[url]

    async def send(self, *args: Any, resolve: bool = True, **kwargs: Any) -> Any:
        response = await self._send(**kwargs)
        if resolve:
            response.data = await self._expand_nested(response.data)

        return response

    @property
    def url_params(self) -> dict:
        return dict(
            sysparm_offset=self.offset,
            sysparm_limit=self.limit,
            sysparm_query=self.query,
            **super().url_params,
        )
