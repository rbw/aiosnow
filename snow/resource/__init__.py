from __future__ import annotations

from typing import TYPE_CHECKING, Any, AsyncGenerator, Type, Union
from urllib.parse import urlencode, urljoin

import marshmallow

from snow.config import ConfigSchema
from snow.consts import Joined
from snow.exceptions import (
    NoItems,
    PayloadValidationError,
    RequestError,
    SchemaError,
    SelectError,
    SnowException,
    TooManyItems,
)
from snow.request import (
    DeleteRequest,
    GetRequest,
    Pagestream,
    PatchRequest,
    PostRequest,
)
from snow.request.response import Response

from . import fields
from .query import Condition, QueryBuilder, select
from .schema import PartialSchema, Schema, SchemaMeta

if TYPE_CHECKING:
    from snow import Application


class Resource:
    """ServiceNow API Resource Model

    Args:
        schema_cls: Schema class
        app: Application instance

    Attributes:
        config (ConfigSchema): Application config
        url (str): API URL
        fields (dict): Schema fields
    """

    def __init__(self, schema_cls: Type[Schema], app: Application):
        self.app = app
        self.session = app.get_session()

        # Configure self
        self.config = self.app.config

        # Build URL
        url_schema = "https://" if self.config.use_ssl else "http://"
        base_url = url_schema + str(self.config.address)
        self.url = urljoin(base_url, str(schema_cls.Meta.location))

        # Read Resource schema
        self.schema = schema_cls(unknown=marshmallow.EXCLUDE)  # type: Schema
        self.fields = schema_cls.get_fields()
        self.primary_key = self._get_primary_key()
        self._should_resolve = self.__should_resolve

    @property
    def nested_fields(self) -> list:
        return [
            k
            for k, v in self.fields.items()
            if isinstance(v, marshmallow.fields.Nested)
        ]

    @property
    def __should_resolve(self) -> bool:
        for f in self.fields.values():
            if (
                isinstance(f, fields.BaseField) and f.joined != Joined.VALUE
            ) or isinstance(f, marshmallow.fields.Nested):
                return True

        return False

    async def __aenter__(self) -> Resource:
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

    def dumps(self, data: dict) -> str:
        return self.schema.dumps(data)

    @property
    def name(self) -> str:
        return self.schema.__class__.__name__

    def get_url(self, segments: list = None) -> str:
        """Get request URL

        Args:
            segments: Path fragments

        Returns:
            URL
        """

        if segments and not isinstance(segments, list):
            raise SnowException(f"Expected a list of path fragments, got: {segments}")

        params = dict(
            sysparm_fields=",".join(self.fields.keys()),
            sysparm_display_value="all" if self._should_resolve else "false",
        )

        url = self.url

        if segments:
            url += "/" + "/".join(map(str, segments))

        return f"{url}{'?' + urlencode(params) if params else ''}"

    async def stream(
        self, selection: Union[QueryBuilder, None], **kwargs: Any
    ) -> AsyncGenerator:
        """Stream-like async generator

        Fetches data in chunks using the ServiceNow pagination system.

        Chunk size determines the number of records to fetch in one go.
        Setting a lower chunk size decreases memory usage, but increases the
        number of requests sent to the server.

        Keyword Args:
            selection: Snow compatible query
            limit (int): Maximum number of records to return
            offset (int): Starting record index
            chunk_size (int): Number of records to fetch in one go

        Yields:
            Chunk of records
        """

        stream = Pagestream(self, query=select(selection).sysparms, **kwargs)
        while not stream.exhausted:
            async for response in stream.next():
                for record in response.data:
                    yield response, record

    async def get(
        self, selection: Union[QueryBuilder, str] = None, **kwargs: Any
    ) -> Response:
        """Buffered many

        Fetches data and stores in buffer.

        Note: It's recommended to use the stream method when dealing with large
        number of records.

        Keyword Args:
            selection: Snow compatible query
            limit (int): Maximum number of records to return
            offset (int): Starting record index

        Returns:
            Records
        """

        return await GetRequest(self, query=select(selection).sysparms, **kwargs).send()

    async def get_one(self, selection: Union[QueryBuilder, str]) -> Response:
        """Get one record

        Args:
            selection: Snow compatible query

        Returns:
            Record
        """

        if not self.primary_key:
            raise SchemaError(
                f'The selected resource "{self.name}" cannot '
                f'be queried: this schema lacks a field with "is_primary" set'
            )

        response = await self.get(selection, limit=2)
        if len(response) > 1:
            raise TooManyItems("Too many results: expected one, got at least 2")
        elif len(response) < 1:
            raise NoItems("Expected a single object in response, got none")

        return response[0]

    async def get_pk_value(self, sysparm_query: str) -> str:
        """Given a query, return the resulting record's PK field's value

        Args:
            sysparm_query: Snow compatible query

        Returns:
            PK field's value
        """

        response = await self.get_one(sysparm_query)
        return response.data[0][self.primary_key]

    async def get_object_id(self, value: Union[Condition, str]) -> str:
        """Get object id by str or Condition

        Immediately return if value is str.

        Args:
            value: Condition or str

        Returns:
            Object id
        """

        if isinstance(value, str):
            return value
        elif isinstance(value, Condition):
            return await self.get_pk_value(value.__str__)
        else:
            raise SelectError(
                f"Selection must be of type {Condition} or {str}, not {type(value)}"
            )

    async def update(self, selection: Union[Condition, str], payload: dict) -> Response:
        """Update matching record

        Args:
            selection: Condition or ID
            payload: Update payload

        Returns:
            Updated record
        """

        object_id = await self.get_object_id(selection)

        if not isinstance(payload, dict):
            raise PayloadValidationError(
                f"Expected payload as a {dict}, got: {type(payload)}"
            )

        try:
            data = self.schema.dumps(payload)
        except marshmallow.exceptions.ValidationError as e:
            raise PayloadValidationError(e)

        return await PatchRequest(self, object_id, data).send()

    async def create(self, payload: dict) -> Response:
        """Create a new record

        Args:
            payload: New record payload

        Returns:
            Created record
        """

        try:
            data = self.schema.dumps(payload)
        except marshmallow.exceptions.ValidationError as e:
            raise PayloadValidationError(e)

        return await PostRequest(self, data).send()

    async def delete(self, selection: Union[Condition, str]) -> Response:
        """Delete matching record

        Args:
            selection: Condition or ID

        Returns:
            dict: {"result": <status>}
        """

        object_id = await self.get_object_id(selection)
        response = await DeleteRequest(self, object_id).send()

        if response.status != 204:
            text = await response.text()
            raise RequestError(
                f"Unexpected response for DELETE request. "
                f"Status: {response.status}, Text: {text}",
                response.status,
            )

        return response
