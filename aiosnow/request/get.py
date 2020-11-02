from time import time
from typing import Any, Generator, Union
from urllib.parse import urlparse

from . import methods
from .base import BaseRequest


class GetRequest(BaseRequest):
    _method = methods.GET
    _cache: dict = {}

    def __init__(
        self,
        *args: Any,
        nested_fields: dict = None,
        limit: int = 10000,
        offset: int = 0,
        query: str = None,
        cache_secs: int = 20,
        **kwargs: Any,
    ):
        self.nested_fields = list(self._nested_with_path(nested_fields or {}, []))
        self._cache_secs = cache_secs
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

    def _nested_with_path(self, fields: dict, path_base: list) -> Generator:
        path = path_base or []

        for k, v in fields.items():
            if not hasattr(v, "nested"):
                continue

            yield path + [k], k, v.schema
            yield from list(
                self._nested_with_path(v.schema.fields, path_base=path + [k])
            )

    async def __expand_document(self, document: dict) -> dict:
        for path, field_name, schema in self.nested_fields:
            if not path or not isinstance(path, list):
                continue

            target_field = path[-1]
            sub_document = document.copy()

            for name in path[:-1]:
                sub_document = sub_document[name]

            if not sub_document.get(target_field):
                continue
            elif "link" not in sub_document[target_field]:
                continue

            nested_data = await self.get_cached(
                sub_document[target_field]["link"], fields=schema.fields.keys()
            )
            sub_document[field_name] = nested_data
            document.update(sub_document)

        return document

    async def _expand_document(
        self, content: Union[dict, list, None]
    ) -> Union[dict, list, None]:
        if not self.nested_fields:
            pass
        elif isinstance(content, dict):
            content = await self.__expand_document(content)
        elif isinstance(content, list):
            for idx, record in enumerate(content):
                content[idx] = await self._expand_document(record)

        return content

    async def get_cached(self, url: str, fields: list = None) -> dict:
        cache_key = hash(url + "".join(fields or []))
        record_id = urlparse(url).path.split("/")[-1]

        if (
            cache_key in self._cache
            and self._cache[cache_key][1] > time() - self._cache_secs
        ):
            self.log.debug(f"Feching {record_id} from cache")
        else:
            request = GetRequest(url, self.session, fields=fields)
            response = await request._send(method=methods.GET)
            self.log.debug(f"Caching response for: {record_id}")
            self._cache[cache_key] = response.data, time()

        return self._cache[cache_key][0]

    async def send(self, *args: Any, resolve: bool = True, **kwargs: Any) -> Any:
        response = await self._send(**kwargs)
        if resolve:
            response.data = await self._expand_document(response.data)

        return response

    @property
    def url_params(self) -> dict:
        return dict(
            sysparm_offset=self.offset,
            sysparm_limit=self.limit,
            sysparm_query=self.query,
            **super().url_params,
        )
