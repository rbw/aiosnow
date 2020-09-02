from __future__ import annotations

from abc import abstractmethod
from typing import Any, Dict, Union

import marshmallow

from aiosnow.config import ConfigSchema
from aiosnow.exceptions import SchemaError
from aiosnow.client import Client
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


class BaseModel(BaseSchema):
    """Abstract base model

    Args:
        client: Client object
    """

    def __init__(
        self,
        client: Client
    ):
        super(BaseSchema, self).__init__(unknown=marshmallow.EXCLUDE)
        self._client = client
        self._primary_key = self._get_primary_key()

    @property
    @abstractmethod
    def _schema_type(self) -> Any:
        pass

    @property
    @abstractmethod
    def api_url(self) -> Any:
        pass

    async def request(self, method: str, *args: Any, **kwargs: Any) -> Response:
        kwargs.update(
            dict(
                api_url=self.api_url,
                session=self._client.get_session(),
                fields=self.Meta.return_only
                or self.fields.keys(),
            )
        )

        req_cls = req_cls_map[method]
        response = await req_cls(*args, **kwargs).send()

        if method != methods.DELETE:
            response.data = self.load(response.data, many=isinstance(response.data, list), partial=True)

        return response

    async def __aenter__(self) -> BaseModel:
        self.session = self._client.get_session()
        return self

    async def __aexit__(self, *_: list) -> None:
        await self.session.close()

    @property
    def _pk_candidates(self) -> list:
        return [
            n
            for n, f in self.fields.items()
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

    @property
    def name(self) -> str:
        return self.__class__.__name__
