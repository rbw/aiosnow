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

from .schema import ModelSchema, ModelSchemaMeta, Nested
from .schema.fields import BaseField

req_cls_map = {
    methods.GET: GetRequest,
    methods.POST: PostRequest,
    methods.PATCH: PatchRequest,
    methods.DELETE: DeleteRequest,
}


class BaseModelMeta(type):
    def __new__(mcs, name: str, bases: tuple, attrs: dict) -> Any:
        attrs["fields"] = fields = {}
        base_members = {}

        for base in bases:
            base_members.update(
                {
                    k: v
                    for k, v in base.__dict__.items()
                    if not isinstance(v, (BaseField, Nested, ModelSchemaMeta))
                }
            )
            inherited_fields = getattr(base.schema_cls, "_declared_fields")
            fields.update(inherited_fields)

        for k, v in attrs.items():
            if isinstance(v, (BaseField, Nested, ModelSchemaMeta)):
                if k in base_members.keys():
                    raise InvalidFieldName(
                        f"Field :{name}.{k}: conflicts with a base member, name it something else. "
                        f"The Field :attribute: parameter can be used to give a field an alias."
                    )

                fields[k] = v

        # Create the Model Schema
        attrs["schema_cls"] = type(name + "Schema", (ModelSchema,), attrs["fields"])
        return super().__new__(mcs, name, bases, attrs)


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
        self.schema = self.schema_cls(unknown=marshmallow.EXCLUDE)
        self.nested_fields = getattr(self.schema, "nested_fields")
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
