from __future__ import annotations

from typing import Any, AsyncGenerator, Type, Union

import aiohttp
import marshmallow

from snow.config import ConfigSchema
from snow.exceptions import (
    NoItems,
    PayloadValidationError,
    RequestError,
    SchemaError,
    SelectError,
    TooManyItems,
    UnexpectedModelSchema,
    UnexpectedResponseContent,
)
from snow.model import BaseModel
from snow.query import Condition, QueryBuilder, select
from snow.request import Pagestream, Response, methods

from .schema import TableSchema


class TableModel(BaseModel):
    """Table API model

    Args:
        schema_cls: Schema class
        instance_url: Instance URL
        session: Snow-compatible aiohttp.ClientSession
        config: Config object

    Attributes:
        config (ConfigSchema): Application config
        api_url (str): Table API URL
        instance_url (str): Instance URL
        session (ClientSession): Session for performing requests
        schema (Schema): Resource Schema
        fields (dict): Fields declared in Schema
        primary_key (str): Schema primary key
    """

    _schema_type = TableSchema

    def __init__(
        self,
        schema_cls: Type[TableSchema],
        instance_url: str,
        session: aiohttp.ClientSession,
        config: ConfigSchema,
    ):
        super(TableModel, self).__init__(schema_cls, instance_url, session, config)
        meta = self.schema.snow_meta
        if not getattr(meta, "table_name", None) or not meta.table_name:
            raise UnexpectedModelSchema(
                f"Missing Meta.table_name in {self.__class__.__name__}"
            )

        self.nested_fields = self._nested_fields

    @property
    def api_url(self) -> str:
        return self.instance_url + "/api/now/table/" + self.schema.snow_meta.table_name

    @property
    def _nested_fields(self) -> dict:
        nested = {}
        for k, v in self.fields.items():
            if not isinstance(v, marshmallow.fields.Nested):
                continue

            nested_cls = getattr(v, "nested")
            nested[k] = nested_cls.get_fields()

        return nested

    async def stream(
        self, selection: Union[QueryBuilder, str] = None, **kwargs: Any
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

        stream = Pagestream(
            api_url=self.api_url,
            query=select(selection).sysparms,
            session=self.session,
            fields=self.fields.keys(),
            nested_fields=self.nested_fields,
            **kwargs,
        )

        while not stream.exhausted:
            async for response in stream.get_next():
                response.data = self._deserialize(response.data)
                for record in response.data:
                    yield response, record

    async def get_one(self, selection: Union[QueryBuilder, str]) -> dict:
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
        if not isinstance(response.data, list):
            raise UnexpectedResponseContent(
                f"Expected a {list} in response to get_one(), got: {type(response.data)}",
                status=response.status,
            )
        elif len(response) > 1:
            raise TooManyItems("Too many results: expected one, got at least 2")
        elif len(response) < 1:
            raise NoItems("Expected a single object in response, got none")

        return response.data[0]

    async def get_pk_value(self, sysparm_query: str) -> str:
        """Given a query, return the resulting record's PK field's value

        Args:
            sysparm_query: Snow compatible query

        Returns:
            PK field's value
        """

        response = await self.get_one(sysparm_query)
        return response[self.primary_key]

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
            Response
        """

        return await self.request(
            methods.GET,
            query=select(selection).sysparms,
            nested_fields=self.nested_fields,
            **kwargs,
        )

    async def update(self, selection: Union[Condition, str], payload: dict) -> Response:
        """Update matching record

        Args:
            selection: Condition or ID of object to update
            payload: Update payload

        Returns:
            Response
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

        return await self.request(methods.PATCH, object_id=object_id, payload=data,)

    async def create(self, payload: dict) -> Response:
        """Create a new record

        Args:
            payload: New record payload

        Returns:
            Response
        """

        try:
            data = self.schema.dumps(payload)
        except marshmallow.exceptions.ValidationError as e:
            raise PayloadValidationError(e)

        return await self.request(methods.POST, payload=data,)

    async def delete(self, selection: Union[Condition, str]) -> Response:
        """Delete matching record

        Args:
            selection: Condition or ID

        Returns:
            Response
        """

        object_id = await self.get_object_id(selection)
        response = await self.request(methods.DELETE, object_id=object_id,)

        if response.status != 204:
            text = await response.text()
            raise RequestError(
                f"Unexpected response for DELETE request. "
                f"Status: {response.status}, Text: {text}",
                response.status,
            )

        return response
