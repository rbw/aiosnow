from __future__ import annotations

from abc import abstractmethod
from typing import Any, Type

import aiohttp
import marshmallow

from aiosnow.client import Client
from aiosnow.exceptions import InvalidFieldName
from aiosnow.request import (
    DeleteRequest,
    GetRequest,
    PatchRequest,
    PostRequest,
    Response,
    methods,
)

from .schema import ModelSchema, Nested
from .schema.fields import BaseField

req_cls_map = {
    methods.GET: GetRequest,
    methods.POST: PostRequest,
    methods.PATCH: PatchRequest,
    methods.DELETE: DeleteRequest,
}


class BaseModelMeta(type):
    def __new__(mcs, name: str, bases: tuple, attrs: dict) -> Any:
        fields = {}

        for base in bases:
            fields.update(base.schema_cls._declared_fields)

        for key, value in attrs.copy().items():
            if isinstance(value, BaseField):
                fields[key] = value
                fields[key].name = key
            elif isinstance(value, marshmallow.schema.SchemaMeta):
                fields[key] = Nested(key, value, allow_none=True, required=False)
            else:
                continue

            # Do not allow override of base members with schema Field attributes.
            for base in bases:
                existing_member = getattr(base, key, None)
                if existing_member is not None and not issubclass(
                    existing_member.__class__,
                    (BaseField, marshmallow.schema.SchemaMeta),
                ):
                    raise InvalidFieldName(
                        f"Field :{name}.{key}: conflicts with a base member, name it something else. "
                        f"The Field :attribute: parameter can be used to give a field an alias."
                    )

        attrs["schema_cls"] = type(name + "Schema", (ModelSchema,), fields)
        cls = super().__new__(mcs, name, bases, attrs)

        return cls


class BaseModel(metaclass=BaseModelMeta):
    """Model base"""

    _session: aiohttp.ClientSession
    _client: Client
    _config: dict = {"return_only": []}
    schema_cls: Type[ModelSchema]
    schema: ModelSchema

    def __init__(self, client: Client):
        self._client = client
        self.fields = dict(self.schema_cls.fields)
        self.nested_fields = {
            n: f for n, f in self.fields.items() if isinstance(f, Nested)
        }
        self.schema = self.schema_cls(unknown=marshmallow.EXCLUDE)
        self._primary_key = getattr(self.schema, "_primary_key")

    @property
    @abstractmethod
    def _api_url(self) -> Any:
        pass

    async def request(self, method: str, *args: Any, **kwargs: Any) -> Response:
        kwargs.update(
            dict(
                api_url=self._api_url,
                session=self._session,
                fields=kwargs.pop("return_only", self._config["return_only"])
                or self.fields.keys(),
            )
        )

        req_cls = req_cls_map[method]
        response = await req_cls(*args, **kwargs).send()

        if method != methods.DELETE:
            response.data = self.schema.load_content(
                response.data, many=isinstance(response.data, list)
            )

        return response

    async def __aenter__(self) -> BaseModel:
        self._session = self._client.get_session()
        return self

    async def __aexit__(self, *_: list) -> None:
        await self._session.close()
