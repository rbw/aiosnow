from __future__ import annotations

from abc import abstractmethod
from typing import Any, Dict, Type, Union

import aiohttp
import marshmallow

from aiosnow.config import ConfigSchema
from aiosnow.exceptions import SchemaError, UnexpectedModelSchema
from aiosnow.request import (
    DeleteRequest,
    GetRequest,
    PatchRequest,
    PostRequest,
    Response,
    methods,
)

from .schema import BaseSchema, fields

req_cls_map = {
    methods.GET: GetRequest,
    methods.POST: PostRequest,
    methods.PATCH: PatchRequest,
    methods.DELETE: DeleteRequest,
}


class BaseModel:
    """Abstract base model

    Args:
        schema_cls: Schema class
        instance_url: Instance URL
        session: aiosnow-compatible aiohttp.ClientSession
        config: Config object

    Attributes:
        config (ConfigSchema): Client config
        session (ClientSession): Session for performing requests
        schema (Schema): Resource Schema
        instance_url (str): Instance URL
        primary_key (str): Schema primary key
    """

    def __init__(
        self,
        schema_cls: Type[BaseSchema],
        instance_url: str,
        session: aiohttp.ClientSession,
        config: ConfigSchema,
    ):
        if not issubclass(schema_cls, self._schema_type):
            raise UnexpectedModelSchema(
                f"Unexpected Schema: {schema_cls.__name__}, Model: "
                f"{self.__class__.__name__}, must be subclass of: {self._schema_type.__name__}"
            )

        self.session = session
        self.config = config
        self.instance_url = instance_url

        # Read Schema
        self.schema = schema_cls(unknown=marshmallow.EXCLUDE)
        self.primary_key = self._get_primary_key()

    @property
    @abstractmethod
    def _schema_type(self) -> Any:
        pass

    @property
    @abstractmethod
    def api_url(self) -> Any:
        pass

    def _deserialize(self, content: Union[dict, list]) -> Union[dict, list]:
        if not isinstance(content, (dict, list)):
            raise ValueError(f"Cannot deserialize type {type(content)}")

        return self.schema.load(content, many=isinstance(content, list), partial=True)

    async def request(self, method: str, *args: Any, **kwargs: Any) -> Response:
        kwargs.update(
            dict(
                api_url=self.api_url,
                session=self.session,
                fields=self.schema.aiosnow_meta.return_only
                or self.schema.fields.keys(),
            )
        )

        req_cls = req_cls_map[method]
        response = await req_cls(*args, **kwargs).send()

        if method != methods.DELETE:
            response.data = self._deserialize(response.data)

        return response

    async def __aenter__(self) -> BaseModel:
        return self

    async def __aexit__(self, *_: list) -> None:
        await self.session.close()

    @property
    def _pk_candidates(self) -> list:
        return [
            n
            for n, f in self.schema.fields.items()
            if isinstance(f, fields.BaseField) and f.is_primary is True
        ]

    def _get_primary_key(self) -> Union[str, None]:
        pks = self._pk_candidates

        if len(pks) > 1:
            raise SchemaError(
                f"Multiple primary keys (is_primary) supplied "
                f"in {self.name}. Maximum allowed is 1."
            )
        elif len(pks) == 0:
            return None

        return pks[0]

    def dumps(self, data: Dict[Any, Any]) -> str:
        return self.schema.dumps(data)

    @property
    def name(self) -> str:
        return self.schema.__class__.__name__
